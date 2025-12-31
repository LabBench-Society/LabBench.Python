import pytest

@pytest.mark.unittest
def test_version_matches_pyproject():
    import labbench_comm
    from importlib.metadata import version

    assert labbench_comm.__version__ == version("labbench_comm")
