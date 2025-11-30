from base64 import (
    b16decode,
    b16encode,
    b32decode,
    b32encode,
    b64decode,
    b64encode,
    b85decode,
    b85encode,
    urlsafe_b64decode,
    urlsafe_b64encode,
)
from typing import Generic, TypeVar

from typing_extensions import Self

from snowflake_id_toolkit._config import SnowflakeIDConfig

TConfig = TypeVar("TConfig", bound=SnowflakeIDConfig)


class SnowflakeID(int, Generic[TConfig]):
    """Base class for snowflake-like ID.

    Uses a configuration class to define bit layout and time resolution.
    Subclasses must set _config_cls to a class implementing SnowflakeIDConfig.
    """

    _config_cls: type[TConfig]

    def timestamp_ms(self, epoch: int = 0) -> int:
        """
        Extract timestamp in milliseconds since Unix epoch.
        """

        timestamp_shift = self._config_cls.SEQUENCE_BITS + self._config_cls.NODE_ID_BITS
        timestamp_mask = (1 << self._config_cls.TIMESTAMP_BITS) - 1
        relative_timestamp = (int(self) >> timestamp_shift) & timestamp_mask
        return (relative_timestamp * self._config_cls.TIME_STEP_MS) + epoch

    def node_id(self) -> int:
        """
        Extract node ID component from ID.
        """

        node_id_shift = self._config_cls.SEQUENCE_BITS
        node_id_mask = (1 << self._config_cls.NODE_ID_BITS) - 1
        return (int(self) >> node_id_shift) & node_id_mask

    def sequence(self) -> int:
        """
        Extract sequence component from ID.
        """

        sequence_mask = (1 << self._config_cls.SEQUENCE_BITS) - 1
        return int(self) & sequence_mask

    def as_bytes(self) -> bytes:
        """
        Convert ID to 8-byte representation.
        """

        return self.to_bytes(8, "big", signed=False)

    @classmethod
    def parse_bytes(cls, data: bytes) -> Self:
        """
        Parse ID from 8-byte representation.
        """

        return cls.from_bytes(data, "big", signed=False)

    def as_base16(self) -> bytes:
        """
        Encode ID as base16 (hexadecimal).
        """

        return b16encode(self.as_bytes())

    @classmethod
    def parse_base16(cls, data: bytes) -> Self:
        """
        Parse ID from base16 (hexadecimal).
        """

        return cls.parse_bytes(b16decode(data))

    def as_base32(self) -> bytes:
        """
        Encode ID as base32.
        """

        return b32encode(self.as_bytes())

    @classmethod
    def parse_base32(cls, data: bytes) -> Self:
        """
        Parse ID from base32.
        """

        return cls.parse_bytes(b32decode(data))

    def as_base64(self) -> bytes:
        """
        Encode ID as base64.
        """

        return b64encode(self.as_bytes())

    @classmethod
    def parse_base64(cls, data: bytes) -> Self:
        """
        Parse ID from base64.
        """

        return cls.parse_bytes(b64decode(data))

    def as_base64_urlsafe(self) -> bytes:
        """
        Encode ID as URL-safe base64.
        """

        return urlsafe_b64encode(self.as_bytes())

    @classmethod
    def parse_base64_urlsafe(cls, data: bytes) -> Self:
        """
        Parse ID from URL-safe base64.
        """

        return cls.parse_bytes(urlsafe_b64decode(data))

    def as_base85(self) -> bytes:
        """
        Encode ID as base85.
        """

        return b85encode(self.as_bytes())

    @classmethod
    def parse_base85(cls, data: bytes) -> Self:
        """
        Parse ID from base85.
        """

        return cls.parse_bytes(b85decode(data))
