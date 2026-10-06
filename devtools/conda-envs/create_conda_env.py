"""Create an owner environment with supported Python and strict priority."""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import tomllib
from pathlib import Path
from tempfile import TemporaryDirectory

import yaml
from packaging.specifiers import SpecifierSet

ROOT = Path(__file__).resolve().parents[2]


def selected_environment(path: Path, python: str, *, root: Path = ROOT) -> dict:
    """Keep dependencies and reject Python outside this owner's source contract."""
    project = tomllib.loads((root / "pyproject.toml").read_text())["project"]
    if not re.fullmatch(r"[0-9]+\.[0-9]+", python) or python not in SpecifierSet(
        project["requires-python"]
    ):
        raise ValueError("Selected Python minor is outside the source contract")
    if path.name == "development_env.yaml" and python != "3.14":
        raise ValueError("Routine development requires Python 3.14")
    content = yaml.safe_load(path.read_text())
    items = content.get("dependencies")
    if not isinstance(items, list):
        raise ValueError("Environment needs a dependencies list")
    content["dependencies"] = ["python=" + python] + [
        value
        for value in items
        if not isinstance(value, str) or not re.match(r"^python(?:$|[ =<>])", value)
    ]
    return content


def manager() -> str:
    command = shutil.which("mamba") or shutil.which("conda")
    if not command:
        raise ValueError("Install Conda or Mamba before creating an environment")
    return command


def create_environment(path: Path, name: str, python: str) -> None:
    """Clean temporary YAML on success/failure and propagate creation errors."""
    content = selected_environment(path, python)
    with TemporaryDirectory(prefix="lindelint-environment-") as temporary:
        recipe = Path(temporary) / "environment.yaml"
        recipe.write_text(yaml.safe_dump(content, sort_keys=False))
        subprocess.run(
            [manager(), "env", "create", "--name", name, "--file", str(recipe)],
            check=True,
            env={**os.environ, "CONDA_CHANNEL_PRIORITY": "strict"},
        )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-n", "--name", required=True)
    parser.add_argument("-p", "--python", default="3.14")
    parser.add_argument("conda_file", type=Path)
    args = parser.parse_args()
    try:
        create_environment(args.conda_file.resolve(), args.name, args.python)
    except (OSError, ValueError, yaml.YAMLError, subprocess.SubprocessError) as exc:
        print(f"Environment creation: FAIL — {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
