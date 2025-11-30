from snowflake_id_toolkit._config import SnowflakeIDConfig

# Instagram Snowflake ID configuration
# Bit layout (64 bits total):
#     [41 bits timestamp][13 bits node ID][10 bits sequence]
INSTAGRAM_SNOWFLAKE_CONFIG = SnowflakeIDConfig(
    timestamp_bits=41,
    node_id_bits=13,
    sequence_bits=10,
)
