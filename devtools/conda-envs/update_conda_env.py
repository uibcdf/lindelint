"""Update the active environment with strict priority and propagated failures."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

import yaml
from create_conda_env import manager, selected_environment


def update_environment(path: Path) -> None:
    content = selected_environment(
        path, f"{sys.version_info.major}.{sys.version_info.minor}"
    )
    with TemporaryDirectory(prefix="lindelint-update-") as temporary:
        recipe = Path(temporary) / "environment.yaml"
        recipe.write_text(yaml.safe_dump(content, sort_keys=False))
        subprocess.run(
            [
                manager(),
                "env",
                "update",
                "--prefix",
                sys.prefix,
                "--file",
                str(recipe),
                "--prune",
            ],
            check=True,
            env={**os.environ, "CONDA_CHANNEL_PRIORITY": "strict"},
        )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("conda_file", type=Path)
    args = parser.parse_args()
    try:
        update_environment(args.conda_file.resolve())
    except (OSError, ValueError, yaml.YAMLError, subprocess.SubprocessError) as exc:
        print(f"Environment update: FAIL — {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
