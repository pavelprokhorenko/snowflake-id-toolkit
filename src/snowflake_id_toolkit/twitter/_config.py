from snowflake_id_toolkit._config import SnowflakeIDConfig


class TwitterSnowflakeConfig(SnowflakeIDConfig):
    """Configuration for Twitter Snowflake ID format.

    Bit layout (64 bits total):
        [1 bit unused][41 bits timestamp][10 bits node ID][12 bits sequence]
    """

    TIMESTAMP_BITS = 41
    NODE_ID_BITS = 10
    SEQUENCE_BITS = 12
