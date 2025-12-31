

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