import threading
import time
from typing import Generic, TypeVar

from snowflake_id_toolkit._config import SnowflakeIDConfig
from snowflake_id_toolkit._exceptions import (
    LastGenerationTimestampIsGreaterError,
    MaxTimestampHasReachedError,
)
from snowflake_id_toolkit._id import SnowflakeID

TID = TypeVar("TID", bound=SnowflakeID)


class SnowflakeIDGenerator(Generic[TID]):
    """Base class for snowflake-like ID generators.

    Uses a configuration instance to define bit layout and time resolution.
    Subclasses must set _config and _id_cls.
    """

    _config: SnowflakeIDConfig

    _id_cls: type[TID]

    def __init__(
        self,
        node_id: int,
        *,
        epoch: int = 0,
    ) -> None:
        """Initialize the generator.

        Args:
            node_id: Unique identifier for this node/machine.
            epoch: Custom epoch timestamp in milliseconds (default: Unix epoch).

        Raises:
            ValueError: If node_id or epoch is out of valid range.
            MaxTimestampHasReachedError: If current time exceeds max representable.
        """

        if not 0 <= node_id <= self._config.max_node_id:
            raise ValueError(f"Node ID must be between 0 and {self._config.max_node_id}")

        if not 0 <= epoch <= self._config.max_timestamp:
            raise ValueError(f"Epoch must be between 0 and {self._config.max_timestamp}")

        current_timestamp = self._get_current_timestamp()

        if epoch > current_timestamp:
            raise ValueError("Epoch cannot be in the future")

        if current_timestamp - epoch > self._config.max_timestamp:
            raise MaxTimestampHasReachedError

        self._lock = threading.Lock()

        self._node_id = node_id
        self._epoch = epoch
        self._sequence = 0
        self._last_generation_timestamp = current_timestamp

    def generate_next_id(self) -> TID:
        """Generate the next unique snowflake ID.

        Returns:
            A unique SnowflakeID instance.

        Raises:
            MaxTimestampHasReachedError: If timestamp exceeds max representable.
            LastGenerationTimestampIsGreaterError: If clock moved backwards.
        """

        with self._lock:
            current_timestamp = self._get_current_timestamp()

            if current_timestamp - self._epoch > self._config.max_timestamp:
                raise MaxTimestampHasReachedError

            if current_timestamp == self._last_generation_timestamp:
                if self._sequence == self._config.max_sequence:
                    # Wait for the next timestamp
                    while current_timestamp == self._last_generation_timestamp:
                        current_timestamp = self._get_current_timestamp()
                self._sequence += 1
            elif current_timestamp > self._last_generation_timestamp:
                self._sequence = 0
            else:
                raise LastGenerationTimestampIsGreaterError

            self._last_generation_timestamp = current_timestamp

            return self._id_cls(
                (current_timestamp - self._epoch) << self._config.timestamp_shift
                | self._node_id << self._config.node_id_shift
                | self._sequence
            )

    @classmethod
    def _get_current_timestamp(cls) -> int:
        return time.time_ns() // (1_000_000 * cls._config.time_step_ms)
