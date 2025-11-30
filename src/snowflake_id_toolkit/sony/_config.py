from snowflake_id_toolkit._config import SnowflakeIDConfig


class SonyflakeConfig(SnowflakeIDConfig):
    """Configuration for Sonyflake ID format.

    Bit layout (64 bits total):
        [1 bit unused][39 bits timestamp][8 bits node ID][16 bits sequence]
    """

    TIMESTAMP_BITS = 39
    NODE_ID_BITS = 8
    SEQUENCE_BITS = 16

    TIME_STEP_MS = 10
