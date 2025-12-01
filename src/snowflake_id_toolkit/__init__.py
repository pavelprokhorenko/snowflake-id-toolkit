"""
Snowflake ID Toolkit - Generate distributed unique IDs.
"""

from snowflake_id_toolkit._config import SnowflakeIDConfig
from snowflake_id_toolkit._exceptions import (
    LastGenerationTimestampIsGreaterError,
    MaxTimestampHasReachedError,
)
from snowflake_id_toolkit._generator import SnowflakeIDGenerator
from snowflake_id_toolkit._id import SnowflakeID
from snowflake_id_toolkit.instagram import InstagramSnowflakeID, InstagramSnowflakeIDGenerator
from snowflake_id_toolkit.sony import SonyflakeID, SonyflakeIDGenerator
from snowflake_id_toolkit.twitter import TwitterSnowflakeID, TwitterSnowflakeIDGenerator

__all__ = (
    "InstagramSnowflakeID",
    "InstagramSnowflakeIDGenerator",
    "LastGenerationTimestampIsGreaterError",
    "MaxTimestampHasReachedError",
    "SnowflakeID",
    "SnowflakeIDConfig",
    "SnowflakeIDGenerator",
    "SonyflakeID",
    "SonyflakeIDGenerator",
    "TwitterSnowflakeID",
    "TwitterSnowflakeIDGenerator",
    "__version__",
)

# Version will be set dynamically by hatch-vcs
__version__ = "0.0.0"
