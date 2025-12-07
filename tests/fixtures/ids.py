import pytest

from snowflake_id_toolkit.instagram import InstagramSnowflakeID, InstagramSnowflakeIDGenerator
from snowflake_id_toolkit.sony import SonyflakeID, SonyflakeIDGenerator
from snowflake_id_toolkit.twitter import TwitterSnowflakeID, TwitterSnowflakeIDGenerator


@pytest.fixture
def twitter_id(twitter_generator: TwitterSnowflakeIDGenerator) -> TwitterSnowflakeID:
    """Create a sample TwitterSnowflakeID."""
    return twitter_generator.generate_next_id()


@pytest.fixture
def instagram_id(instagram_generator: InstagramSnowflakeIDGenerator) -> InstagramSnowflakeID:
    """Create a sample InstagramSnowflakeID."""
    return instagram_generator.generate_next_id()


@pytest.fixture
def sonyflake_id(sonyflake_generator: SonyflakeIDGenerator) -> SonyflakeID:
    """Create a sample SonyflakeID."""
    return sonyflake_generator.generate_next_id()
