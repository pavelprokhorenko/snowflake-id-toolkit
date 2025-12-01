from snowflake_id_toolkit._generator import SnowflakeIDGenerator
from snowflake_id_toolkit.sony._config import SONYFLAKE_CONFIG
from snowflake_id_toolkit.sony._id import SonyflakeID


class SonyflakeIDGenerator(SnowflakeIDGenerator[SonyflakeID]):
    """Sony's Sonyflake ID generator.

    Generates 64-bit IDs that are roughly time-sortable with extended lifespan.

    Bit layout (64 bits total):
        [1 bit unused][39 bits timestamp][8 bits node ID][16 bits sequence]

    Key characteristics:
        - Time resolution: 10 milliseconds (vs 1ms for Twitter/Instagram)
        - Extended epoch coverage: ~174 years (vs ~69 years for Twitter/Instagram)
        - Higher throughput: 65,536 IDs per 10ms interval per node (vs 4096 IDs per ms for Twitter/Instagram)
        - Compact node space: 256 nodes (suitable for smaller deployments)

    Why 10ms is better than 1ms for most applications:
        1. Sufficient precision: Most applications don't need sub-10ms ordering granularity.
           Human-perceivable events, API requests, database operations, and business logic
           rarely require microsecond-level timestamp precision.

        2. Extended lifespan: By using 10ms intervals instead of 1ms, Sonyflake achieves
           174 years of coverage (vs 69 years with 1ms). This means your system can run
           without epoch resets for 2.5x longer - critical for long-term infrastructure.

        3. Better throughput: With 16 sequence bits, you get 65,536 IDs per 10ms window
           (6.5M IDs/sec per node). This is 16x more than Twitter's 4,096 IDs/ms capacity,
           reducing sequence overflow scenarios during burst traffic.

        4. Clock skew tolerance: 10ms granularity provides better resilience against minor
           clock drift and NTP adjustments. Small clock corrections are less likely to cause
           timestamp collisions or "clock moved backward" errors.

        5. Fewer sequence resets: Longer time windows mean sequences reset less frequently,
           resulting in better ID distribution and reduced contention on sequence counters.

    Capacity:
        - ~174 years of timestamps (from epoch) with 10ms precision
        - 256 unique nodes (2^8)
        - 65,536 IDs per 10ms interval per node (2^16)

    Use cases:
        - Systems requiring extended epoch lifespan
        - Ultra-high throughput per node requirements
        - Deployments with ≤256 nodes
        - Applications tolerant of 10ms timestamp precision

    Example:
        >>> generator = SonyflakeIDGenerator(
        ...     node_id=0, epoch=173568960000
        ... )
        >>> generator.generate_next_id()
    """

    _config = SONYFLAKE_CONFIG

    _id_cls = SonyflakeID
