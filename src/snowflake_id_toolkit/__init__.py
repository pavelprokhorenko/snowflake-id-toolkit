"""
Snowflake ID Toolkit - Generate distributed unique IDs.
"""

from snowflake_id_toolkit._exceptions import (
    LastGenerationTimestampIsGreaterError,
    MaxSequenceHasReachedError,
    MaxTimestampHasReachedError,
)
from snowflake_id_toolkit._generator import SnowflakeIDGenerator
from snowflake_id_toolkit.twitter import TwitterSnowflakeIDGenerator

__all__ = (
    "LastGenerationTimestampIsGreaterError",
    "MaxSequenceHasReachedError",
    "MaxTimestampHasReachedError",
    "SnowflakeIDGenerator",
    "TwitterSnowflakeIDGenerator",
    "__version__",
)

# Version will be set dynamically by hatch-vcs
__version__ = "0.0.0"
