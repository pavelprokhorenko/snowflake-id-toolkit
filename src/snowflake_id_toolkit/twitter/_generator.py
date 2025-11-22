from snowflake_id_toolkit._generator import SnowflakeIDGenerator


class TwitterSnowflakeIDGenerator(SnowflakeIDGenerator):
    """Twitter's Snowflake ID generator.

    Generates 64-bit IDs that are roughly time-sortable.

    Bit layout (64 bits total):
        [1 bit unused][41 bits timestamp][10 bits node ID][12 bits sequence]

    Capacity:
        - ~69 years of timestamps (from epoch)
        - 1024 unique nodes
        - 4096 IDs per millisecond per node

    Example:
        >>> generator = TwitterSnowflakeIDGenerator(
        ...     node_id=0, epoch=1288834974657
        ... )
        >>> generator.generate_next_id()
    """

    _TIMESTAMP_BITS = 41
    _NODE_ID_BITS = 10
    _SEQUENCE_BITS = 12
