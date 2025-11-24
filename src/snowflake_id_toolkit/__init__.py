"""
Snowflake ID Toolkit - Generate distributed unique IDs.
"""

from snowflake_id_toolkit._exceptions import (
    LastGenerationTimestampIsGreaterError,
    MaxTimestampHasReachedError,
)
from snowflake_id_toolkit._generator import SnowflakeIDGenerator
from snowflake_id_toolkit.instagram import InstagramSnowflakeIDGenerator
from snowflake_id_toolkit.sony import SonyflakeIDGenerator
from snowflake_id_toolkit.twitter import TwitterSnowflakeIDGenerator

__all__ = (
    "InstagramSnowflakeIDGenerator",
    "LastGenerationTimestampIsGreaterError",
    "MaxTimestampHasReachedError",
    "SnowflakeIDGenerator",
    "SonyflakeIDGenerator",
    "TwitterSnowflakeIDGenerator",
    "__version__",
)

# Version will be set dynamically by hatch-vcs
__version__ = "0.0.0"
