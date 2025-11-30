from snowflake_id_toolkit._config import SnowflakeIDConfig

# Sonyflake ID configuration
# Bit layout (64 bits total):
#     [1 bit unused][39 bits timestamp][8 bits node ID][16 bits sequence]
SONYFLAKE_CONFIG = SnowflakeIDConfig(
    timestamp_bits=39,
    node_id_bits=8,
    sequence_bits=16,
    time_step_ms=10,
)
