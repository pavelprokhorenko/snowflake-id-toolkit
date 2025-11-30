from snowflake_id_toolkit._id import SnowflakeID
from snowflake_id_toolkit.twitter._config import TWITTER_SNOWFLAKE_CONFIG


class TwitterSnowflakeID(SnowflakeID):
    """Twitter Snowflake ID.

    A 64-bit integer ID that encodes timestamp, node ID, and sequence number.

    Bit layout (64 bits total):
        [1 bit unused][41 bits timestamp][10 bits node ID][12 bits sequence]
    """

    _config = TWITTER_SNOWFLAKE_CONFIG
