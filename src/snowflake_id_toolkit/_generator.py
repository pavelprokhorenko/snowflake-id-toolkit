import time
from typing import Final

from snowflake_id_toolkit._exceptions import (
    LastGenerationTimestampIsGreaterError,
    MaxSequenceHasReachedError,
    MaxTimestampHasReachedError,
)


class SnowflakeIDGenerator:
    _TIMESTAMP_BITS: int
    _NODE_ID_BITS: int
    _SEQUENCE_BITS: int

    _TIME_STEP_MS: int = 1

    def __init__(
        self,
        node_id: int,
        *,
        epoch: int = 0,
    ) -> None:
        self._NODE_ID_SHIFT: Final[int] = self._SEQUENCE_BITS
        self._TIMESTAMP_SHIFT: Final[int] = self._NODE_ID_BITS + self._NODE_ID_SHIFT

        self._MAX_TIMESTAMP: Final[int] = -1 ^ (-1 << self._TIMESTAMP_BITS)
        self._MAX_NODE_ID: Final[int] = -1 ^ (-1 << self._NODE_ID_BITS)
        self._MAX_SEQUENCE: Final[int] = -1 ^ (-1 << self._SEQUENCE_BITS)

        if not 0 <= node_id <= self._MAX_NODE_ID:
            raise ValueError(f"Node ID must be between 0 and {self._MAX_NODE_ID}")

        if not 0 <= epoch <= self._MAX_TIMESTAMP:
            raise ValueError(f"Epoch must be between 0 and {self._MAX_TIMESTAMP}")

        current_timestamp = self._get_current_timestamp()

        if epoch > current_timestamp:
            raise ValueError("Epoch cannot be in the future")

        if current_timestamp - epoch > self._MAX_TIMESTAMP:
            raise MaxTimestampHasReachedError

        self._node_id = node_id
        self._epoch = epoch
        self._sequence = 0
        self._last_generation_timestamp = current_timestamp

    def generate_next_id(self) -> int:
        current_timestamp = self._get_current_timestamp()

        if current_timestamp - self._epoch > self._MAX_TIMESTAMP:
            raise MaxTimestampHasReachedError

        if current_timestamp == self._last_generation_timestamp:
            if self._sequence == self._MAX_SEQUENCE:
                raise MaxSequenceHasReachedError
            self._sequence += 1
        elif current_timestamp > self._last_generation_timestamp:
            self._sequence = 0
        else:
            raise LastGenerationTimestampIsGreaterError

        self._last_generation_timestamp = current_timestamp

        return (
            (current_timestamp - self._epoch) << self._TIMESTAMP_SHIFT
            | self._node_id << self._NODE_ID_SHIFT
            | self._sequence
        )

    @classmethod
    def _get_current_timestamp(cls) -> int:
        return time.time_ns() // (1_000_000 * cls._TIME_STEP_MS)
