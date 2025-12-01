import pytest


def test_pytest_ok() -> None:
    with pytest.raises(ZeroDivisionError):
        assert 1 / 0
