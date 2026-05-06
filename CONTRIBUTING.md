# Contributing to labbench-comm

Thank you for contributing to **labbench-comm**. This project exists to make reliable, testable, and well-structured communication with LabBench hardware possible in Python.

## Code of Conduct

By participating, you agree to follow the project [Code of Conduct](CODE_OF_CONDUCT.md).

## Development Principles

- Async-first I/O
- Protocol correctness over convenience
- Explicit state and wire formats
- Focused, testable changes
- Hardware tests when hardware behavior changes
- No circular dependencies
- Pythonic APIs with deterministic protocol behavior

## Setup

This project uses a `src/` layout, so the package must be installed into the Python environment that runs tests or examples.

From the repository root:

```bash
python -m pip install -e .[dev]
```

If you see `ModuleNotFoundError: No module named 'labbench_comm'`, install the package into the current environment with the command above.

## Tests

Run unit tests:

```bash
python -m pytest -m unittest -v
```

Run hardware tests only when compatible hardware is connected:

```bash
python -m pytest -m hardware -v
```

Test markers:

| Marker | Description |
| --- | --- |
| `unittest` | Unit tests that do not require physical hardware |
| `hardware` | Tests that require connected LabBench hardware |
| `cpar` | CPAR+ hardware/integration tests |

## Examples

Examples also require the editable install because of the `src/` layout:

```bash
python -m pip install -e .[dev]
python examples/lio/device_overview.py --port COM3
```

Some examples drive hardware outputs. Read the example and verify the connected setup before running output-driving scripts.

## Build

Install build tools:

```bash
python -m pip install --upgrade build setuptools wheel twine
```

Build and verify:

```bash
python -m build
twine check dist/*
```

You can inspect the wheel contents with:

```bash
python -m zipfile -l dist/labbench_comm-[VERSION]-py3-none-any.whl
```

Check that package modules under `labbench_comm/` are included and tests are not included.

## Pull Requests

- Keep changes focused.
- Add or update tests for behavioral changes.
- Update README/examples/docs for user-facing changes.
- Note whether hardware testing was performed.
- Do not include build artifacts, virtual environments, or cache files.
