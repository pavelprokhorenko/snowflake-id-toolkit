from snowflake_id_toolkit._config import SnowflakeIDConfig

# Twitter Snowflake ID configuration
# Bit layout (64 bits total):
#     [1 bit unused][41 bits timestamp][10 bits node ID][12 bits sequence]
TWITTER_SNOWFLAKE_CONFIG = SnowflakeIDConfig(
    timestamp_bits=41,
    node_id_bits=10,
    sequence_bits=12,
)
