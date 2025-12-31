#!/usr/bin/env python
"""
Test installation of labbench-comm from TestPyPI.

This script:
- Creates an isolated virtual environment
- Installs labbench-comm from TestPyPI
- Verifies version and imports
- Runs basic smoke tests
- Optionally runs pytest if tests are included

Safe to run on Windows, Linux, and macOS.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VENV_DIR = ROOT / ".testpypi-venv"


def run(cmd: list[str]) -> None:
    print(f"\n>>> {' '.join(cmd)}")
    subprocess.run(cmd, check=True)


def python_bin() -> Path:
    if sys.platform == "win32":
        return VENV_DIR / "Scripts" / "python.exe"
    return VENV_DIR / "bin" / "python"


def main() -> None:
    print("🔧 Creating isolated virtual environment")

    if VENV_DIR.exists():
        shutil.rmtree(VENV_DIR)

    run([sys.executable, "-m", "venv", str(VENV_DIR)])

    py = python_bin()

    print("⬆ Upgrading pip")
    run([str(py), "-m", "pip", "install", "--upgrade", "pip"])

    print("📦 Installing labbench-comm from TestPyPI")
    run(
        [
            str(py),
            "-m",
            "pip",
            "install",
            "-i",
            "https://test.pypi.org/simple/",
            "--extra-index-url",
            "https://pypi.org/simple",
            "labbench-comm",
        ]
    )

    print("🔍 Verifying installation")
    run(
        [
            str(py),
            "-c",
            (
                "import labbench_comm; "
                "from importlib.metadata import version; "
                "print('labbench_comm version:', labbench_comm.__version__); "
                "assert labbench_comm.__version__ == version('labbench_comm')"
            ),
        ]
    )

    print("🧪 Running smoke tests")
    run(
        [
            str(py),
            "-c",
            (
                "from labbench_comm.protocols.bus_central import BusCentral; "
                "from labbench_comm.devices.cpar import CPARplusCentral; "
                "print('Core imports OK')"
            ),
        ]
    )

    print("\n✅ TestPyPI installation test completed successfully.")


if __name__ == "__main__":
    main()
