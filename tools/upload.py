#!/usr/bin/env python3
"""
Build and upload labbench_comm to PyPI with version guard.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path
from importlib.metadata import version as pkg_version


PACKAGE_NAME = "labbench_comm"

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"
BUILD = ROOT / "build"


def run(cmd: list[str]) -> None:
    print(">", " ".join(cmd))
    subprocess.run(cmd, check=True)


def pypi_version_exists(pkg: str, ver: str) -> bool:
    """
    Check if a version already exists on PyPI.
    """
    url = f"https://pypi.org/pypi/{pkg}/json"
    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            data = json.load(resp)
    except Exception:
        # Package does not exist yet
        return False

    return ver in data.get("releases", {})


def main() -> None:
    local_version = pkg_version(PACKAGE_NAME)
    print(f"Local version: {local_version}")

    if pypi_version_exists(PACKAGE_NAME, local_version):
        print(
            f"❌ Version {local_version} already exists on PyPI.\n"
            f"➡️  Bump the version before uploading."
        )
        sys.exit(1)

    #print("Cleaning old artifacts...")
    #shutil.rmtree(DIST, ignore_errors=True)
    #shutil.rmtree(BUILD, ignore_errors=True)
    #
    #for egg in ROOT.glob("*.egg-info"):
    #    shutil.rmtree(egg, ignore_errors=True)
    #
    #print("Building package...")
    #run([sys.executable, "-m", "build"])
    #
    #print("Running twine checks...")
    #run([sys.executable, "-m", "twine", "check", "dist/*"])

    print("Uploading to PyPI...")
    run([sys.executable, "-m", "twine", "upload", "dist/*"])

    print("✅ Upload complete")


if __name__ == "__main__":
    main()
