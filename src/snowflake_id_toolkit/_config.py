from dataclasses import dataclass
from functools import cached_property


@dataclass(frozen=True)
class SnowflakeIDConfig:
    """Configuration for snowflake-like ID.

    Attributes:
        timestamp_bits: Number of bits for timestamp.
        node_id_bits: Number of bits for node/machine ID.
        sequence_bits: Number of bits for sequence number.
        time_step_ms: Time resolution in milliseconds (default: 1).
    """

    timestamp_bits: int
    node_id_bits: int
    sequence_bits: int

    time_step_ms: int = 1

    @cached_property
    def node_id_shift(self) -> int:
        return self.sequence_bits

    @cached_property
    def timestamp_shift(self) -> int:
        return self.node_id_bits + self.node_id_shift

    @cached_property
    def max_timestamp(self) -> int:
        return -1 ^ (-1 << self.timestamp_bits)

    @cached_property
    def max_node_id(self) -> int:
        return -1 ^ (-1 << self.node_id_bits)

    @cached_property
    def max_sequence(self) -> int:
        return -1 ^ (-1 << self.sequence_bits)
