import pytest

from snowflake_id_toolkit.instagram import InstagramSnowflakeIDGenerator
from snowflake_id_toolkit.sony import SonyflakeIDGenerator
from snowflake_id_toolkit.twitter import TwitterSnowflakeIDGenerator


@pytest.fixture
def twitter_generator() -> TwitterSnowflakeIDGenerator:
    """Create a TwitterSnowflakeIDGenerator with node_id=0."""
    return TwitterSnowflakeIDGenerator(node_id=0)


@pytest.fixture
def instagram_generator() -> InstagramSnowflakeIDGenerator:
    """Create an InstagramSnowflakeIDGenerator with node_id=0."""
    return InstagramSnowflakeIDGenerator(node_id=0)


@pytest.fixture
def sonyflake_generator() -> SonyflakeIDGenerator:
    """Create a SonyflakeIDGenerator with node_id=0."""
    return SonyflakeIDGenerator(node_id=0)


@pytest.fixture
def twitter_generators_multi_node() -> list[TwitterSnowflakeIDGenerator]:
    """Create multiple TwitterSnowflakeIDGenerator instances with node_ids 3, 4, 5."""
    return [TwitterSnowflakeIDGenerator(node_id=i) for i in range(3, 6)]


@pytest.fixture
def instagram_generators_multi_node() -> list[InstagramSnowflakeIDGenerator]:
    """Create multiple InstagramSnowflakeIDGenerator instances with node_ids 3, 4, 5."""
    return [InstagramSnowflakeIDGenerator(node_id=i) for i in range(3, 6)]


@pytest.fixture
def sonyflake_generators_multi_node() -> list[SonyflakeIDGenerator]:
    """Create multiple SonyflakeIDGenerator instances with node_ids 3, 4, 5."""
    return [SonyflakeIDGenerator(node_id=i) for i in range(3, 6)]
