# Contributing to labbench-comm

First of all: **thank you for contributing** to *labbench-comm*.  
This project exists to make reliable, testable, and well-structured communication with LabBench hardware possible in Python, and contributions are very welcome.

This document explains **how to contribute safely and effectively**, following best practices for open-source Python projects.

---

## Code of Conduct

By participating in this project, you agree to act professionally and respectfully.

- Be constructive and respectful
- Assume good intent
- Focus on technical merit
- No harassment, discrimination, or personal attacks

If problems arise, please contact the maintainers via GitHub Issues.

---

## Project Philosophy

Before contributing, it helps to understand the guiding principles:

- **Async-first**: all I/O must be non-blocking and asyncio-compatible
- **Protocol correctness over convenience**
- **Explicit over implicit** (clear state machines, no magic)
- **Testability is mandatory**
- **Hardware tests are optional but encouraged**
- **No circular dependencies**
- **Pythonic, but deterministic**

---


## Development setup

This project uses a modern **`src/` layout**, which means the package must be installed before it can be imported (including by tests).

If you see an error like:
* ModuleNotFoundError: No module named 'labbench_comm'


it means the package has not yet been installed into your current Python environment.

### Editable (development) install

From the project root (the directory containing `pyproject.toml`), run:

```bash
python -m pip install -e .[dev]
```

This installs `labbench-comm` in editable mode and with development dependencies, so any changes you make to the source code are immediately reflected without reinstalling.


### Running tests

Once the package is installed, run the unit test suite with:

```
python -m pytest -m [testtype] -v
```

Using `python -m pytest` ensures that tests are executed using the same Python environment into which the package was installed.

Test type defines the test suite being run:

| testtype | Description |
|----------|-------------|
| unittest | |
| cpar     | |

## Building the package

### Prerequisites (one-time)

Prerequisites (one-time)

```
python -m pip install --upgrade build setuptools wheel
```



### Building the package

```
python -m build
```

### Verify the package content (optional but recommended)

You can inspect the wheel:

```
python -m zipfile -l dist/labbench_comm-[VERSION NUMBER]-py3-none-any.whl
```

Check the following:

* labbench_comm/devices/... is included
* labbench_comm/protocols, serial, utils are included
* No tests/ inside the wheel


