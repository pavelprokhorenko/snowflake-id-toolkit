from snowflake_id_toolkit._generator import SnowflakeIDGenerator


class TwitterSnowflakeIDGenerator(SnowflakeIDGenerator):
    _TIMESTAMP_BITS = 41
    _NODE_ID_BITS = 10
    _SEQUENCE_BITS = 12
