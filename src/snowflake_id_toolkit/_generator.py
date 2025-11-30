import threading
import time
from typing import Final, Generic, TypeVar

from snowflake_id_toolkit._config import SnowflakeIDConfig
from snowflake_id_toolkit._exceptions import (
    LastGenerationTimestampIsGreaterError,
    MaxTimestampHasReachedError,
)

TConfig = TypeVar("TConfig", bound=SnowflakeIDConfig)


class SnowflakeIDGenerator(Generic[TConfig]):
    """Base class for snowflake-like ID generators.

    Uses a configuration class to define bit layout and time resolution.
    Subclasses must set _config_cls to a class implementing SnowflakeIDConfig.
    """

    _config_cls: type[TConfig]

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

        self._NODE_ID_SHIFT: Final[int] = self._config_cls.SEQUENCE_BITS
        self._TIMESTAMP_SHIFT: Final[int] = self._config_cls.NODE_ID_BITS + self._NODE_ID_SHIFT

        self._MAX_TIMESTAMP: Final[int] = -1 ^ (-1 << self._config_cls.TIMESTAMP_BITS)
        self._MAX_NODE_ID: Final[int] = -1 ^ (-1 << self._config_cls.NODE_ID_BITS)
        self._MAX_SEQUENCE: Final[int] = -1 ^ (-1 << self._config_cls.SEQUENCE_BITS)

        if not 0 <= node_id <= self._MAX_NODE_ID:
            raise ValueError(f"Node ID must be between 0 and {self._MAX_NODE_ID}")

        if not 0 <= epoch <= self._MAX_TIMESTAMP:
            raise ValueError(f"Epoch must be between 0 and {self._MAX_TIMESTAMP}")

        current_timestamp = self._get_current_timestamp()

        if epoch > current_timestamp:
            raise ValueError("Epoch cannot be in the future")

        if current_timestamp - epoch > self._MAX_TIMESTAMP:
            raise MaxTimestampHasReachedError

        self._lock = threading.Lock()

        self._node_id = node_id
        self._epoch = epoch
        self._sequence = 0
        self._last_generation_timestamp = current_timestamp

    def generate_next_id(self) -> int:
        """Generate the next unique snowflake ID.

        Returns:
            A unique 64-bit integer ID.

        Raises:
            MaxTimestampHasReachedError: If timestamp exceeds max representable.
            LastGenerationTimestampIsGreaterError: If clock moved backwards.
        """

        with self._lock:
            current_timestamp = self._get_current_timestamp()

            if current_timestamp - self._epoch > self._MAX_TIMESTAMP:
                raise MaxTimestampHasReachedError

            if current_timestamp == self._last_generation_timestamp:
                if self._sequence == self._MAX_SEQUENCE:
                    # Wait for the next timestamp
                    while current_timestamp == self._last_generation_timestamp:
                        current_timestamp = self._get_current_timestamp()
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
        return time.time_ns() // (1_000_000 * cls._config_cls.TIME_STEP_MS)
