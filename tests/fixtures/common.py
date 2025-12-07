from collections.abc import Generator
from typing import cast

import pytest
from freezegun import freeze_time
from freezegun.api import FrozenDateTimeFactory


@pytest.fixture
def frozen_time() -> Generator[FrozenDateTimeFactory]:
    """
    Freeze time at a fixed point for deterministic testing.
    """

    with freeze_time("2025-01-01 00:00:00") as frozen:
        yield cast(
            FrozenDateTimeFactory,
            frozen,
        )
