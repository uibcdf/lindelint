"""Verify that a Lindelint wheel contains its required private package."""

from __future__ import annotations

import sys
from pathlib import Path
from zipfile import ZipFile


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: check_wheel.py path/to/lindelint.whl", file=sys.stderr)
        return 2
    wheel = Path(sys.argv[1])
    with ZipFile(wheel) as archive:
        names = set(archive.namelist())
    required = "lindelint/_private/smonitor/__init__.py"
    if required not in names:
        print(f"{wheel}: missing {required}", file=sys.stderr)
        return 1
    print(f"{wheel}: contains {required}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
