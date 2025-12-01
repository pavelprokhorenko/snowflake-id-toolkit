import pytest

from snowflake_id_toolkit._config import SnowflakeIDConfig


@pytest.fixture
def config_twitter_like() -> SnowflakeIDConfig:
    """Create a Twitter-like SnowflakeIDConfig (41-10-12, 1ms resolution)."""
    return SnowflakeIDConfig(
        timestamp_bits=41,
        node_id_bits=10,
        sequence_bits=12,
    )


@pytest.fixture
def config_sonyflake_like() -> SnowflakeIDConfig:
    """Create a Sonyflake-like SnowflakeIDConfig (39-8-16, 10ms resolution)."""
    return SnowflakeIDConfig(
        timestamp_bits=39,
        node_id_bits=8,
        sequence_bits=16,
        time_step_ms=10,
    )
