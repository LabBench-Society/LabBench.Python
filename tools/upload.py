#!/usr/bin/env python
"""
Upload the labbench-comm package to TestPyPI.

Prerequisites:
- dist/ directory exists (run tools/build.py first)
- ~/.pypirc is configured with a [testpypi] entry
- twine is installed

This script is intentionally explicit and safe.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"


def run(cmd: list[str]) -> None:
    print(f"\n>>> {' '.join(cmd)}")
    subprocess.run(cmd, check=True)


def main() -> None:
    if not DIST.exists():
        print("❌ dist/ directory not found. Run tools/build.py first.")
        sys.exit(1)

    files = list(DIST.glob("*"))
    if not files:
        print("❌ dist/ is empty. Nothing to upload.")
        sys.exit(1)

    print("📦 Files to upload:")
    for f in files:
        print(f"  - {f.name}")

    run(
        [
            sys.executable,
            "-m",
            "twine",
            "upload",
            "dist/*",
            "--verbose"
        ]
    )

    print("\n✅ Upload to TestPyPI completed successfully.")
    print("🔗 https://pypi.org/project/labbench-comm/")


if __name__ == "__main__":
    main()
