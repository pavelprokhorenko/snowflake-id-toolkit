from snowflake_id_toolkit._id import SnowflakeID
from snowflake_id_toolkit.instagram._config import INSTAGRAM_SNOWFLAKE_CONFIG


class InstagramSnowflakeID(SnowflakeID):
    """Instagram Snowflake ID.

    A 64-bit integer ID that encodes timestamp, node ID, and sequence number.

    Bit layout (64 bits total):
        [41 bits timestamp][13 bits node ID][10 bits sequence]
    """

    _config = INSTAGRAM_SNOWFLAKE_CONFIG
