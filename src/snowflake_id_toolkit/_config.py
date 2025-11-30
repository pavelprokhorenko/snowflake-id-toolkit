from typing import ClassVar


class SnowflakeIDConfig:
    """Abstract base class for snowflake-like ID configuration.

    Subclasses must define:
        TIMESTAMP_BITS: Number of bits for timestamp.
        NODE_ID_BITS: Number of bits for node/machine ID.
        SEQUENCE_BITS: Number of bits for sequence number.
        TIME_STEP_MS: Time resolution in milliseconds (default: 1).
    """

    TIMESTAMP_BITS: ClassVar[int]
    NODE_ID_BITS: ClassVar[int]
    SEQUENCE_BITS: ClassVar[int]

    TIME_STEP_MS: ClassVar[int] = 1
