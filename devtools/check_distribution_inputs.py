"""Run the reviewed suite dependency/resource audit before tests or publication."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def checked_provider(root: Path, suite: Path) -> Path:
    """Require the immutable reviewed SDK before executing any of its code."""
    expected = tomllib.loads((root / "devtools/dependency_routes.toml").read_text())[
        "shared_tool"
    ]["commit"]
    head = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=suite, text=True
    ).strip()
    if not re.fullmatch(r"[0-9a-f]{40}", expected) or head != expected:
        raise ValueError("Use the reviewed full MolSysSuite provider commit")
    subprocess.run(["git", "diff", "--quiet", "HEAD", "--"], cwd=suite, check=True)
    if subprocess.check_output(
        ["git", "status", "--porcelain", "--untracked-files=all", "--", "devtools"],
        cwd=suite,
        text=True,
    ).strip():
        raise ValueError("Shared distribution tooling is modified or untracked")
    return suite / "devtools/scripts/dependency_routes.py"


def check_resources(root: Path) -> None:
    """Require every tracked runtime file, including the private diagnostic package."""
    inventory = tomllib.loads(
        (root / "devtools/conda-build/resources.toml").read_text()
    )
    paths = subprocess.check_output(
        ["git", "ls-files", "-z", "--", "lindelint"], cwd=root
    )
    expected = {"site-packages/" + p.decode() for p in paths.split(b"\0") if p}
    expected.add("site-packages/lindelint/_version.py")
    if set(inventory["required_paths"]) != expected:
        raise ValueError("Review all tracked runtime files in the resource inventory")


def check_candidate(root: Path, candidate: str, version: str) -> None:
    """Require a real committed owner decision; the example cannot authorize a build."""
    if not re.fullmatch(r"[0-9a-f]{40}", candidate):
        raise ValueError("Candidate must be a full lowercase commit SHA")
    head = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=root, text=True
    ).strip()
    if head != candidate:
        raise ValueError("Candidate differs from the checked-out source")
    subprocess.run(["git", "diff", "--quiet", "HEAD", "--"], cwd=root, check=True)
    plan_path = "devtools/conda-build/release_plan.toml"
    subprocess.run(
        ["git", "ls-files", "--error-unmatch", plan_path],
        cwd=root,
        check=True,
        capture_output=True,
    )
    plan = tomllib.loads((root / plan_path).read_text())
    reviewed = tomllib.loads(
        (root / "devtools/conda-build/release_plan.example.toml").read_text()
    )
    for field in (
        "required_workflows",
        "gate_jobs",
        "test_platforms",
        "python_versions",
    ):
        if plan.get(field) != reviewed[field]:
            raise ValueError(
                f"Review candidate gate or matrix changes before publication: {field}"
            )
    if plan["version"] != version or not re.fullmatch(
        r"(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)", version
    ):
        raise ValueError("Reviewed release version differs from the candidate")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--suite-root", type=Path, required=True)
    parser.add_argument("--declared-only", action="store_true")
    parser.add_argument("--candidate-sha")
    parser.add_argument("--version")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        root = args.root.resolve()
        tool = checked_provider(root, args.suite_root.resolve())
        check_resources(root)
        subprocess.run(
            [
                sys.executable,
                str(root / "devtools/broadcast_requirements.py"),
                "--check",
                "--root",
                str(root),
            ],
            check=True,
        )
        if args.candidate_sha or args.version:
            if not args.candidate_sha or not args.version:
                raise ValueError("Candidate and version must be supplied together")
            check_candidate(root, args.candidate_sha, args.version)
        command = [sys.executable, str(tool), "--root", str(root)]
        if args.declared_only:
            command.append("--declared-only")
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        receipt = json.loads(result.stdout)
        expected = (
            "declared-only"
            if args.declared_only
            else "declared-and-installed-public-bounds"
        )
        if receipt.get("qualification") != expected:
            raise ValueError(
                "Shared tool returned an incomplete dependency qualification"
            )
        if args.output:
            args.output.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
    except (OSError, ValueError, KeyError, subprocess.SubprocessError) as exc:
        print(f"Distribution input review: FAIL — {exc}", file=sys.stderr)
        if isinstance(exc, subprocess.CalledProcessError) and exc.stderr:
            print(exc.stderr.strip(), file=sys.stderr)
        return 1
    print(
        json.dumps(
            {
                "scope": expected,
                "candidate": args.candidate_sha,
                "routes": len(receipt["routes"]),
                "installed_versions": receipt.get("installed_versions", {}),
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
