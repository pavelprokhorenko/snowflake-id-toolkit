from snowflake_id_toolkit._generator import SnowflakeIDGenerator
from snowflake_id_toolkit.twitter._config import TwitterSnowflakeConfig


class TwitterSnowflakeIDGenerator(SnowflakeIDGenerator[TwitterSnowflakeConfig]):
    """Twitter's Snowflake ID generator.

    Generates 64-bit IDs that are roughly time-sortable.

    Bit layout (64 bits total):
        [1 bit unused][41 bits timestamp][10 bits node ID][12 bits sequence]

    Capacity:
        - ~69 years of timestamps (from epoch)
        - 1024 unique nodes (2^10)
        - 4096 IDs per millisecond per node (2^12)

    Example:
        >>> generator = TwitterSnowflakeIDGenerator(
        ...     node_id=0, epoch=1288834974657
        ... )
        >>> generator.generate_next_id()
    """

    _config_cls = TwitterSnowflakeConfig
