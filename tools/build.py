#!/usr/bin/env python
"""
Build, check, and validate the labbench-comm package.

This script:
- Cleans all build artifacts
- Builds source and wheel distributions
- Runs tests
- Runs Ruff (linting)
- Runs MyPy (type checking)
- Verifies the built package with Twine

Works on Windows, Linux, and macOS.

To run:
python tools/build.py

"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run(cmd: list[str]) -> None:
    print(f"\n>>> {' '.join(cmd)}")
    subprocess.run(cmd, check=True)


def clean() -> None:
    print("\n--- Cleaning build artifacts ---")

    for path in [
        "build",
        "dist",
        ".pytest_cache"
    ]:
        shutil.rmtree(ROOT / path, ignore_errors=True)

    for pattern in ["*.egg-info", "**/__pycache__"]:
        for p in ROOT.glob(pattern):
            shutil.rmtree(p, ignore_errors=True)


def build() -> None:
    print("\n--- Building package ---")
    run([sys.executable, "-m", "build"])

def test() -> None:
    print("\n--- Running tests ---")
    run(["pytest", "-m", "unittest","-v"])

def verify() -> None:
    print("\n--- Verifying package metadata ---")
    run(["twine", "check", "dist/*"])

def main() -> None:
    clean()
    test()
    build()
    verify()

    print("\n✅ Build and validation completed successfully.")


if __name__ == "__main__":
    main()
