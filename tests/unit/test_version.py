from importlib.metadata import version
import pytest
import labbench_comm

@pytest.mark.unittest
def test_version_matches_pyproject() -> None:
    assert labbench_comm.__version__ == version("labbench_comm")
