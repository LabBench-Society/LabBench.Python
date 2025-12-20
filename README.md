

## Development setup

This project uses a modern **`src/` layout**, which means the package must be installed before it can be imported (including by tests).

If you see an error like:
* ModuleNotFoundError: No module named 'labbench_comm'


it means the package has not yet been installed into your current Python environment.

### Editable (development) install

From the project root (the directory containing `pyproject.toml`), run:

```bash
python -m pip install -e .
```

This installs `labbench-comm` in editable mode, so any changes you make to the source code are immediately reflected without reinstalling.

To install development dependencies (such as pytest) at the same time, run:

```bash
python -m pip install -e .[dev]
```

Running tests

Once the package is installed, run the test suite with:

```
python -m pytest
```

Using `python -m pytest` ensures that tests are executed using the same Python environment into which the package was installed.