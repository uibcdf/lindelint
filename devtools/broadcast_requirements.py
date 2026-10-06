"""Generate Conda environments from metadata and owner tooling; preserve the recipe."""

from __future__ import annotations

import argparse
import sys
import tomllib
from pathlib import Path

import yaml
from packaging.requirements import Requirement
from packaging.utils import canonicalize_name

ROOT = Path(__file__).resolve().parents[1]
GROUPS = {
    "production": "production",
    "development": "development",
    "test": "test",
    "docs": "docs",
    "setup": "setup",
    "build": "conda-build",
}


def flatten(values: list) -> list[str]:
    """Flatten the existing YAML anchor groups without executing configuration."""
    result = []
    for value in values:
        items = flatten(value) if isinstance(value, list) else [value]
        for item in items:
            if not isinstance(item, str) or not item.strip():
                raise ValueError("Requirement groups need nonempty strings")
            if item not in result:
                result.append(item)
    return result


def environment_documents(root: Path) -> dict[str, str]:
    """Derive required names/bounds from pyproject; keep owner tool selections."""
    project = tomllib.loads((root / "pyproject.toml").read_text())["project"]
    groups = yaml.safe_load((root / "devtools/requirements.yaml").read_text())
    required_names = {
        canonicalize_name(Requirement(value).name) for value in project["dependencies"]
    }
    documents = {}
    for name, group in GROUPS.items():
        record = groups[group]
        channels = flatten(record["channels"])
        if channels != ["uibcdf", "conda-forge"]:
            raise ValueError("Environment channels must be uibcdf then conda-forge")
        python = (
            "python=3.14"
            if name == "development"
            else "python " + project["requires-python"]
        )
        dependencies = [python]
        if name not in {"setup", "build"}:
            dependencies.extend(project["dependencies"])
        for value in flatten(record["dependencies"]):
            # Metadata owns Python and required runtime constraints. Groups own tools.
            if value.split()[0].split("=")[0] == "python":
                continue
            if (
                name not in {"setup", "build"}
                and canonicalize_name(Requirement(value).name) in required_names
            ):
                continue
            if value not in dependencies:
                dependencies.append(value)
        documents[f"devtools/conda-envs/{name}_env.yaml"] = yaml.safe_dump(
            {"channels": channels, "dependencies": dependencies}, sort_keys=False
        )
    return documents


def generate(root: Path, *, check: bool = False) -> None:
    """Write only managed environment files, or reject drift without mutation."""
    documents = environment_documents(root)
    changed = [
        name
        for name, text in documents.items()
        if not (root / name).is_file() or (root / name).read_text() != text
    ]
    if check and changed:
        raise ValueError("Generated environments differ: " + ", ".join(changed))
    if not check:
        for name in changed:
            (root / name).write_text(documents[name])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        generate(args.root.resolve(), check=args.check)
    except (OSError, ValueError, KeyError, TypeError, yaml.YAMLError) as exc:
        print(f"Environment generation: FAIL — {exc}", file=sys.stderr)
        return 1
    print("Generated environment inputs: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
