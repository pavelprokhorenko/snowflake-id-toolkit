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

        current_timestamp = self.get_current_timestamp()

        if not 0 <= epoch <= current_timestamp:
            raise ValueError("Epoch must be between 0 and current timestamp")

        if current_timestamp - epoch > self._config.max_timestamp:
            raise MaxTimestampHasReachedError

        self._lock = threading.Lock()

        self._node_id = node_id
        self._epoch = epoch
        self._sequence = 0
        self._last_generation_timestamp = -1

    def generate_next_id(self) -> TID:
        """Generate the next unique snowflake ID.

        Returns:
            A unique SnowflakeID instance.

        Raises:
            MaxTimestampHasReachedError: If timestamp exceeds max representable.
            LastGenerationTimestampIsGreaterError: If clock moved backwards.
        """

        with self._lock:
            current_timestamp = self.get_current_timestamp()

            if current_timestamp - self._epoch > self._config.max_timestamp:
                raise MaxTimestampHasReachedError

            if current_timestamp == self._last_generation_timestamp:
                if self._sequence == self._config.max_sequence:
                    # Wait for the next timestamp
                    current_timestamp = self._wait_for_next_timestamp()
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

    def _wait_for_next_timestamp(self) -> int:
        """Wait until the next timestamp becomes available.

        This method busy-waits until the current timestamp advances beyond
        the last generation timestamp. It's extracted as a separate method
        to facilitate testing.

        Returns:
            The next timestamp that is greater than last_timestamp.
        """
        current_timestamp = self.get_current_timestamp()
        while current_timestamp == self._last_generation_timestamp:
            current_timestamp = self.get_current_timestamp()
        return current_timestamp

    @classmethod
    def get_current_timestamp(cls) -> int:
        """Get the current timestamp in the appropriate units for this generator.

        For generators with 1ms resolution (Twitter, Instagram), returns milliseconds.
        For generators with 10ms resolution (Sonyflake), returns 10-millisecond units.

        This method should be used when setting a custom epoch to ensure the correct
        time resolution is used for each generator type.

        Returns:
            Current timestamp in generator-specific units.

        Example:
            >>> # For Twitter/Instagram (1ms resolution)
            >>> current_epoch = (
            ...     TwitterSnowflakeIDGenerator.get_current_timestamp()
            ... )
            >>> generator = TwitterSnowflakeIDGenerator(
            ...     node_id=0, epoch=current_epoch
            ... )
            >>>
            >>> # For Sonyflake (10ms resolution)
            >>> current_epoch = SonyflakeIDGenerator.get_current_timestamp()
            >>> generator = SonyflakeIDGenerator(
            ...     node_id=0, epoch=current_epoch
            ... )
        """

        return time.time_ns() // (1_000_000 * cls._config.time_step_ms)
