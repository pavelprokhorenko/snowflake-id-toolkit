import pytest

from snowflake_id_toolkit._config import SnowflakeIDConfig
from snowflake_id_toolkit.instagram import INSTAGRAM_SNOWFLAKE_CONFIG
from snowflake_id_toolkit.sony import SONYFLAKE_CONFIG
from snowflake_id_toolkit.twitter import TWITTER_SNOWFLAKE_CONFIG


def test_config_initialization_valid_params(
    config_twitter_like: SnowflakeIDConfig,
) -> None:
    """Test SnowflakeIDConfig initialization with valid parameters."""
    assert config_twitter_like.timestamp_bits == 41
    assert config_twitter_like.node_id_bits == 10
    assert config_twitter_like.sequence_bits == 12
    assert config_twitter_like.time_step_ms == 1


def test_config_initialization_custom_time_step(
    config_sonyflake_like: SnowflakeIDConfig,
) -> None:
    """Test SnowflakeIDConfig initialization with custom time_step_ms."""
    assert config_sonyflake_like.time_step_ms == 10


def test_config_cached_property_node_id_shift(
    config_twitter_like: SnowflakeIDConfig,
) -> None:
    """Test node_id_shift cached property calculation."""
    assert config_twitter_like.node_id_shift == 12


def test_config_cached_property_timestamp_shift(
    config_twitter_like: SnowflakeIDConfig,
) -> None:
    """Test timestamp_shift cached property calculation."""
    assert config_twitter_like.timestamp_shift == 22


def test_config_cached_property_max_timestamp(
    config_twitter_like: SnowflakeIDConfig,
) -> None:
    """Test max_timestamp cached property calculation."""
    assert config_twitter_like.max_timestamp == 2199023255551


def test_config_cached_property_max_node_id(
    config_twitter_like: SnowflakeIDConfig,
) -> None:
    """Test max_node_id cached property calculation."""
    assert config_twitter_like.max_node_id == 1023


def test_config_cached_property_max_sequence(
    config_twitter_like: SnowflakeIDConfig,
) -> None:
    """Test max_sequence cached property calculation."""
    assert config_twitter_like.max_sequence == 4095


def test_config_immutability(
    config_twitter_like: SnowflakeIDConfig,
) -> None:
    """Test SnowflakeIDConfig is immutable (frozen dataclass)."""
    with pytest.raises(AttributeError):
        config_twitter_like.timestamp_bits = 42  # type: ignore[misc]


def test_twitter_config_bit_layout() -> None:
    """Test Twitter Snowflake config has correct bit layout."""
    assert TWITTER_SNOWFLAKE_CONFIG.timestamp_bits == 41
    assert TWITTER_SNOWFLAKE_CONFIG.node_id_bits == 10
    assert TWITTER_SNOWFLAKE_CONFIG.sequence_bits == 12
    assert TWITTER_SNOWFLAKE_CONFIG.time_step_ms == 1


def test_twitter_config_max_values() -> None:
    """Test Twitter Snowflake config calculated max values."""
    assert TWITTER_SNOWFLAKE_CONFIG.max_timestamp == 2199023255551
    assert TWITTER_SNOWFLAKE_CONFIG.max_node_id == 1023
    assert TWITTER_SNOWFLAKE_CONFIG.max_sequence == 4095
    assert TWITTER_SNOWFLAKE_CONFIG.node_id_shift == 12
    assert TWITTER_SNOWFLAKE_CONFIG.timestamp_shift == 22


def test_instagram_config_bit_layout() -> None:
    """Test Instagram Snowflake config has correct bit layout."""
    assert INSTAGRAM_SNOWFLAKE_CONFIG.timestamp_bits == 41
    assert INSTAGRAM_SNOWFLAKE_CONFIG.node_id_bits == 13
    assert INSTAGRAM_SNOWFLAKE_CONFIG.sequence_bits == 10
    assert INSTAGRAM_SNOWFLAKE_CONFIG.time_step_ms == 1


def test_instagram_config_max_values() -> None:
    """Test Instagram Snowflake config calculated max values."""
    assert INSTAGRAM_SNOWFLAKE_CONFIG.max_timestamp == 2199023255551
    assert INSTAGRAM_SNOWFLAKE_CONFIG.max_node_id == 8191
    assert INSTAGRAM_SNOWFLAKE_CONFIG.max_sequence == 1023
    assert INSTAGRAM_SNOWFLAKE_CONFIG.node_id_shift == 10
    assert INSTAGRAM_SNOWFLAKE_CONFIG.timestamp_shift == 23


def test_sonyflake_config_bit_layout() -> None:
    """Test Sonyflake config has correct bit layout."""
    assert SONYFLAKE_CONFIG.timestamp_bits == 39
    assert SONYFLAKE_CONFIG.node_id_bits == 8
    assert SONYFLAKE_CONFIG.sequence_bits == 16
    assert SONYFLAKE_CONFIG.time_step_ms == 10


def test_sonyflake_config_max_values() -> None:
    """Test Sonyflake config calculated max values."""
    assert SONYFLAKE_CONFIG.max_timestamp == 549755813887
    assert SONYFLAKE_CONFIG.max_node_id == 255
    assert SONYFLAKE_CONFIG.max_sequence == 65535
    assert SONYFLAKE_CONFIG.node_id_shift == 16
    assert SONYFLAKE_CONFIG.timestamp_shift == 24


def test_config_different_bit_layouts_produce_different_shifts(
    config_twitter_like: SnowflakeIDConfig,
) -> None:
    """Test different bit layouts produce different shift values."""
    config_instagram_like = SnowflakeIDConfig(
        timestamp_bits=41,
        node_id_bits=13,
        sequence_bits=10,
    )

    assert config_twitter_like.timestamp_shift != config_instagram_like.timestamp_shift
    assert config_twitter_like.node_id_shift != config_instagram_like.node_id_shift
