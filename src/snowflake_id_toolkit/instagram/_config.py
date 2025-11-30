from snowflake_id_toolkit._config import SnowflakeIDConfig


class InstagramSnowflakeConfig(SnowflakeIDConfig):
    """Configuration for Instagram Snowflake ID format.

    Bit layout (64 bits total):
        [41 bits timestamp][13 bits node ID][10 bits sequence]
    """

    TIMESTAMP_BITS = 41
    NODE_ID_BITS = 13
    SEQUENCE_BITS = 10
