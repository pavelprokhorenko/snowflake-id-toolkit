from snowflake_id_toolkit._id import SnowflakeID
from snowflake_id_toolkit.sony._config import SONYFLAKE_CONFIG


class SonyflakeID(SnowflakeID):
    """Sonyflake ID.

    A 64-bit integer ID that encodes timestamp, node ID, and sequence number.

    Bit layout (64 bits total):
        [1 bit unused][39 bits timestamp][8 bits node ID][16 bits sequence]
    """

    _config = SONYFLAKE_CONFIG
