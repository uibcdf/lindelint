"""Exercise owner adapters and the pinned SDK without scientific imports/installations."""

from __future__ import annotations

import importlib.util
import io
import json
import os
import shutil
import subprocess
import sys
import tarfile
import tempfile
import tomllib
import unittest
from pathlib import Path
from unittest.mock import patch

import yaml

ROOT = Path(__file__).resolve().parents[2]
SUITE = Path(os.environ.get("LINDELINT_SUITE_ROOT", ROOT / ".molsyssuite"))


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


broadcast = load("lindelint_broadcast", ROOT / "devtools/broadcast_requirements.py")
review = load("lindelint_review", ROOT / "devtools/check_distribution_inputs.py")
creator = load("create_conda_env", ROOT / "devtools/conda-envs/create_conda_env.py")
sys.modules["create_conda_env"] = creator
updater = load("lindelint_update", ROOT / "devtools/conda-envs/update_conda_env.py")


class TestDistributionInputs(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # A missing provider is a failed gate, never a silently skipped contract.
        review.checked_provider(ROOT, SUITE)
        sys.path.insert(0, str(SUITE))
        from devtools.scripts import dependency_constraints, noarch_conda

        if not Path(noarch_conda.__file__).resolve().is_relative_to(SUITE.resolve()):
            raise AssertionError("Tests resolved another editable SDK namespace")
        cls.noarch = noarch_conda
        cls.constraints = dependency_constraints

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="lindelint-controls-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        for path in (
            "pyproject.toml",
            ".gitignore",
            "devtools",
            ".github",
            "lindelint",
        ):
            source, target = ROOT / path, self.root / path
            if source.is_dir():
                shutil.copytree(
                    source,
                    target,
                    ignore=shutil.ignore_patterns("__pycache__", "_version.py"),
                )
            else:
                shutil.copy2(source, target)
        self.git("init", "-q")
        self.git("config", "user.name", "Contract fixture")
        self.git("config", "user.email", "fixture@example.invalid")
        self.commit()

    def git(self, *args):
        return subprocess.check_output(
            ["git", *args], cwd=self.root, text=True, stderr=subprocess.DEVNULL
        ).strip()

    def commit(self):
        self.git("add", ".")
        self.git("commit", "-qm", "Fixture")
        return self.git("rev-parse", "HEAD")

    def audit(self):
        return subprocess.run(
            [
                sys.executable,
                str(SUITE / "devtools/scripts/dependency_routes.py"),
                "--root",
                str(self.root),
                "--declared-only",
            ],
            capture_output=True,
            text=True,
            check=False,
        )

    def test_current_routes_and_resource_inventory(self):
        result = self.audit()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(len(json.loads(result.stdout)["routes"]), 16)
        review.check_resources(self.root)

    def test_broadcast_preserves_guarded_recipe(self):
        recipe = self.root / "devtools/conda-build/meta.yaml"
        original = recipe.read_bytes()
        broadcast.generate(self.root)
        broadcast.generate(self.root, check=True)
        self.assertEqual(recipe.read_bytes(), original)

    def test_environment_drift_rejected_without_mutation(self):
        path = self.root / "devtools/conda-envs/production_env.yaml"
        path.write_text(path.read_text().replace("- scipy\n", ""))
        before = path.read_bytes()
        with self.assertRaisesRegex(ValueError, "Generated environments differ"):
            broadcast.generate(self.root, check=True)
        self.assertEqual(path.read_bytes(), before)

    def test_future_metadata_floor_propagates_to_runtime_environments(self):
        path = self.root / "pyproject.toml"
        path.write_text(path.read_text().replace('"numpy",', '"numpy>=2",'))
        broadcast.generate(self.root)
        for name in ("production", "development", "test", "docs"):
            dependencies = yaml.safe_load(
                (self.root / f"devtools/conda-envs/{name}_env.yaml").read_text()
            )["dependencies"]
            self.assertIn("numpy>=2", dependencies)
            self.assertNotIn("numpy", dependencies)

    def test_shared_audit_rejects_missing_recipe_requirement(self):
        path = self.root / "devtools/conda-build/meta.yaml"
        path.write_text(path.read_text().replace("    - numpy\n", ""))
        result = self.audit()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("numpy", result.stderr + result.stdout)

    def test_shared_audit_rejects_stale_environment_floor(self):
        metadata = self.root / "pyproject.toml"
        metadata.write_text(metadata.read_text().replace('"numpy",', '"numpy>=2",'))
        recipe = self.root / "devtools/conda-build/meta.yaml"
        recipe.write_text(
            recipe.read_text().replace("    - numpy\n", "    - numpy >=2\n")
        )
        broadcast.generate(self.root)
        self.assertEqual(self.audit().returncode, 0)
        env = self.root / "devtools/conda-envs/test_env.yaml"
        env.write_text(env.read_text().replace("numpy>=2", "numpy>=1"))
        result = self.audit()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("test_env.yaml", result.stderr + result.stdout)

    def test_installed_version_below_public_floor_fails(self):
        project = {"requires-python": ">=3.11,<3.15", "dependencies": ["numpy>=2"]}
        with self.assertRaisesRegex(ValueError, "numpy"):
            self.constraints.check_installed(
                project, version_for=lambda name: "1.99", python_version="3.14.7"
            )
        self.assertEqual(
            self.constraints.check_installed(
                project, version_for=lambda name: "2.4.6", python_version="3.14.7"
            )["numpy"],
            "2.4.6",
        )

    def test_source_candidate_below_public_floor_fails(self):
        from devtools.scripts.dependency_routes import validate_source_version

        with self.assertRaisesRegex(ValueError, "floor|violates|satisfy"):
            validate_source_version("smonitor>=0.19", "0.18.0+local")
        validate_source_version("smonitor>=0.19", "0.19.0+local")

    def test_runtime_inventory_cannot_omit_private_file_or_new_file(self):
        path = self.root / "devtools/conda-build/resources.toml"
        original = path.read_text()
        path.write_text(
            original.replace(
                '  "site-packages/lindelint/_private/smonitor/catalog.py",\n', ""
            )
        )
        with self.assertRaisesRegex(ValueError, "runtime files"):
            review.check_resources(self.root)
        path.write_text(original)
        (self.root / "lindelint/new_resource.txt").write_text("runtime data")
        self.git("add", "lindelint/new_resource.txt")
        with self.assertRaisesRegex(ValueError, "runtime files"):
            review.check_resources(self.root)

    def test_changed_or_unclassified_workflow_fails(self):
        path = self.root / ".github/workflows/CI.yaml"
        path.write_text(path.read_text() + "\n# changed route\n")
        self.assertNotEqual(self.audit().returncode, 0)
        shutil.copy2(ROOT / ".github/workflows/CI.yaml", path)
        (path.parent / "new.yaml").write_text("name: Unreviewed\n")
        self.assertNotEqual(self.audit().returncode, 0)

    def test_real_committed_plan_and_exact_candidate_required(self):
        head = self.git("rev-parse", "HEAD")
        with self.assertRaises(subprocess.CalledProcessError):
            review.check_candidate(self.root, head, "0.0.0")
        plan = self.root / "devtools/conda-build/release_plan.toml"
        shutil.copy2(plan.with_name("release_plan.example.toml"), plan)
        with self.assertRaises(subprocess.CalledProcessError):
            review.check_candidate(self.root, head, "0.0.0")
        head = self.commit()
        review.check_candidate(self.root, head, "0.0.0")
        with self.assertRaisesRegex(ValueError, "differs"):
            review.check_candidate(self.root, "0" * 40, "0.0.0")
        with self.assertRaisesRegex(ValueError, "version differs"):
            review.check_candidate(self.root, head, "0.1.0")
        plan.write_text(
            plan.read_text().replace(
                'python_versions = ["3.11", "3.12", "3.13", "3.14"]',
                'python_versions = ["3.14"]',
            )
        )
        head = self.commit()
        with self.assertRaisesRegex(ValueError, "matrix changes"):
            review.check_candidate(self.root, head, "0.0.0")

    def test_shared_archive_rejects_missing_private_file_and_stale_version(self):
        plan, inventory = self.noarch.inspect_recipe(
            self.root,
            "devtools/conda-build/release_plan.example.toml",
            "devtools/conda-build/resources.toml",
        )
        payload = {name: b"# fixture payload\n" for name in inventory["required_paths"]}
        payload[inventory["version_file"]] = b'__version__ = "0.0.0"\n'
        payload["info/index.json"] = json.dumps(
            {
                "name": "lindelint",
                "version": "0.0.0",
                "build": "py_2",
                "build_number": 2,
                "subdir": "noarch",
                "depends": inventory["expected_run"],
            }
        ).encode()
        payload["info/link.json"] = b'{"noarch": {"type": "python"}}'
        payload["site-packages/lindelint-0.0.0.dist-info/METADATA"] = (
            b"Name: lindelint\nVersion: 0.0.0\n"
        )
        archive = self.root / "lindelint-0.0.0-py_2.tar.bz2"

        def write(entries):
            with tarfile.open(archive, "w:bz2") as target:
                for name, content in entries.items():
                    info = tarfile.TarInfo(name)
                    info.size = len(content)
                    target.addfile(info, io.BytesIO(content))

        write(payload)
        self.noarch.inspect_artifact(archive, plan, inventory)
        missing = "site-packages/lindelint/_private/smonitor/__init__.py"
        write({key: value for key, value in payload.items() if key != missing})
        with self.assertRaisesRegex(ValueError, "missing"):
            self.noarch.inspect_artifact(archive, plan, inventory)
        payload[inventory["version_file"]] = b'__version__ = "9.9.9"\n'
        write(payload)
        with self.assertRaisesRegex(ValueError, "embedded Python version"):
            self.noarch.inspect_artifact(archive, plan, inventory)

    def test_environment_helpers_reject_unsupported_or_nonroutine_python(self):
        production = self.root / "devtools/conda-envs/production_env.yaml"
        for python in ("3.10", "3.15", "3.14; echo unsafe"):
            with self.subTest(python=python), self.assertRaises(ValueError):
                creator.selected_environment(production, python, root=self.root)
        with self.assertRaisesRegex(ValueError, "Routine development"):
            creator.selected_environment(
                production.with_name("development_env.yaml"), "3.13", root=self.root
            )
        self.assertEqual(
            creator.selected_environment(production, "3.14", root=self.root)[
                "dependencies"
            ][0],
            "python=3.14",
        )

    def test_create_and_update_propagate_errors_with_strict_priority_and_cleanup(self):
        path = self.root / "devtools/conda-envs/production_env.yaml"
        for module, operation in (
            (
                creator,
                lambda: creator.create_environment(path, "name with spaces", "3.14"),
            ),
            (updater, lambda: updater.update_environment(path)),
        ):
            observed = []

            def fail(command, **kwargs):
                observed.append(Path(command[command.index("--file") + 1]))
                self.assertTrue(observed[-1].is_file())
                self.assertTrue(kwargs["check"])
                self.assertEqual(kwargs["env"]["CONDA_CHANNEL_PRIORITY"], "strict")
                if module is creator:
                    self.assertEqual(
                        command[command.index("--name") + 1], "name with spaces"
                    )
                raise subprocess.CalledProcessError(9, command)

            with (
                patch.object(module, "manager", return_value="conda"),
                patch.object(module.subprocess, "run", side_effect=fail),
                self.assertRaises(subprocess.CalledProcessError),
            ):
                operation()
            self.assertFalse(observed[0].exists())

    def test_scikit_learn_is_tooling_only(self):
        self.assertNotIn(
            "scikit-learn", (self.root / "devtools/conda-build/meta.yaml").read_text()
        )
        for name in ("production", "test", "development", "docs"):
            requirements = yaml.safe_load(
                (self.root / f"devtools/conda-envs/{name}_env.yaml").read_text()
            )["dependencies"]
            self.assertEqual("scikit-learn" in requirements, name != "production")

    def test_source_preflight_and_installed_science_are_separate(self):
        ci = yaml.safe_load((self.root / ".github/workflows/CI.yaml").read_text())
        steps = ci["jobs"]["test"]["steps"]
        names = [step.get("name") for step in steps]
        self.assertLess(
            names.index("Check distribution inputs"), names.index("Run tests")
        )
        self.assertNotIn(
            "--declared-only", steps[names.index("Check distribution inputs")]["run"]
        )
        self.assertEqual(len(ci["jobs"]["test"]["strategy"]["matrix"]["cfg"]), 8)
        inventory = tomllib.loads(
            (self.root / "devtools/conda-build/resources.toml").read_text()
        )
        self.assertEqual(inventory["installed_tests"]["paths"], ["tests"])
        self.assertEqual(len(inventory["installed_gate"]["required_steps"]), 4)


if __name__ == "__main__":
    unittest.main()
