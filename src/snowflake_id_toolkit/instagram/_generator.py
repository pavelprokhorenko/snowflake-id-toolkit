from snowflake_id_toolkit._generator import SnowflakeIDGenerator


class InstagramSnowflakeIDGenerator(SnowflakeIDGenerator):
    """Instagram's Snowflake ID generator.

    Generates unsigned 64-bit integers that are roughly time-sortable.
    All 64 bits are allocated for ID components (no sign bit).

    Bit layout (64 bits total):
        [41 bits timestamp][13 bits node ID][10 bits sequence]

    Capacity:
        - ~69 years of timestamps (from epoch)
        - 8192 unique nodes (2^13)
        - 1024 IDs per millisecond per node (2^10)

    Example:
        >>> generator = InstagramSnowflakeIDGenerator(
        ...     node_id=0, epoch=1314220021721
        ... )
        >>> generator.generate_next_id()
    """

    _TIMESTAMP_BITS = 41
    _NODE_ID_BITS = 13
    _SEQUENCE_BITS = 10
