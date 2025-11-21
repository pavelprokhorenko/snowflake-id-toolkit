class SnowflakeIDToolkitError(Exception):
    detail: str = "Snowflake ID Toolkit error"

    def __init__(self) -> None:
        super().__init__(self.detail)


class MaxTimestampHasReachedError(OverflowError, SnowflakeIDToolkitError):
    detail: str = "Max timestamp has reached"


class LastGenerationTimestampIsGreaterError(SnowflakeIDToolkitError):
    detail: str = "Last generation timestamp is greater than current timestamp"
