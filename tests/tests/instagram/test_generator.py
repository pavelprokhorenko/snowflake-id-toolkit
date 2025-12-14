import threading
import time
from datetime import timedelta
from unittest import mock

import pytest
from freezegun import freeze_time
from freezegun.api import FrozenDateTimeFactory

from snowflake_id_toolkit import InstagramSnowflakeID
from snowflake_id_toolkit._exceptions import (
    LastGenerationTimestampIsGreaterError,
    MaxTimestampHasReachedError,
)
from snowflake_id_toolkit.instagram import InstagramSnowflakeIDGenerator


# Initialization tests
@pytest.mark.usefixtures("frozen_time")
def test_generator_initialization() -> None:
    generator = InstagramSnowflakeIDGenerator(node_id=100, epoch=1000000000000)
    assert generator._node_id == 100  # noqa: SLF001
    assert generator._epoch == 1000000000000  # noqa: SLF001
    assert generator._sequence == 0  # noqa: SLF001
    assert generator._last_generation_timestamp == -1  # noqa: SLF001


def test_generator_initialization_zero_node_id() -> None:
    generator = InstagramSnowflakeIDGenerator(node_id=0)
    assert generator._node_id == 0  # noqa: SLF001


def test_generator_initialization_max_node_id() -> None:
    # Instagram has 13 bits for node_id, so max is 2^13 - 1 = 8191
    max_node_id = 8191
    generator = InstagramSnowflakeIDGenerator(node_id=max_node_id)
    assert generator._node_id == max_node_id  # noqa: SLF001


@pytest.mark.usefixtures("frozen_time")
def test_generator_initialization_zero_epoch() -> None:
    generator = InstagramSnowflakeIDGenerator(node_id=0, epoch=0)
    assert generator._epoch == 0  # noqa: SLF001


def test_generator_initialization_custom_epoch() -> None:
    custom_epoch = 1609459200000  # 2021-01-01 00:00:00 UTC in ms
    generator = InstagramSnowflakeIDGenerator(node_id=0, epoch=custom_epoch)
    assert generator._epoch == custom_epoch  # noqa: SLF001


# Initialization validation errors
def test_generator_node_id_negative_raises_error() -> None:
    with pytest.raises(ValueError, match=r"Node ID must be between 0 and 8191"):
        InstagramSnowflakeIDGenerator(node_id=-1)


def test_generator_node_id_exceeds_max_raises_error() -> None:
    # Instagram max node_id is 8191
    with pytest.raises(ValueError, match=r"Node ID must be between 0 and 8191"):
        InstagramSnowflakeIDGenerator(node_id=8192)


def test_generator_epoch_negative_raises_error() -> None:
    with pytest.raises(ValueError, match=r"Epoch must be between 0 and current timestamp"):
        InstagramSnowflakeIDGenerator(node_id=0, epoch=-1)


def test_generator_epoch_in_future_raises_error() -> None:
    future_epoch = int(time.time() * 1000) + 1000000
    with pytest.raises(ValueError, match=r"Epoch must be between 0 and current timestamp"):
        InstagramSnowflakeIDGenerator(node_id=0, epoch=future_epoch)


@freeze_time(timedelta(milliseconds=(1 << 41) - 1))
def test_generator_epoch_too_far_in_past_raises_max_timestamp_error() -> None:
    # Instagram has 41 bits for timestamp, max is 2^41 - 1 = 2199023255551 ms
    # If we set epoch too far in the past, current_timestamp - epoch will exceed max
    with pytest.raises(MaxTimestampHasReachedError):
        InstagramSnowflakeIDGenerator(node_id=0, epoch=0)


# ID generation tests
@pytest.mark.usefixtures("frozen_time")
def test_generate_next_id_increments_sequence(instagram_generator: InstagramSnowflakeIDGenerator) -> None:
    id1 = instagram_generator.generate_next_id()
    id2 = instagram_generator.generate_next_id()
    id3 = instagram_generator.generate_next_id()

    assert id1.sequence() == 0
    assert id2.sequence() == 1
    assert id3.sequence() == 2


def test_generate_next_id_unique_ids(instagram_generator: InstagramSnowflakeIDGenerator) -> None:
    ids = [instagram_generator.generate_next_id() for _ in range(100)]
    assert len(ids) == len(set(ids))


def test_generate_next_id_monotonic_increase(instagram_generator: InstagramSnowflakeIDGenerator) -> None:
    """Verify that IDs increase monotonically."""
    ids = [instagram_generator.generate_next_id() for _ in range(100)]
    assert ids == sorted(ids)


def test_generate_next_id_preserves_node_id() -> None:
    generator = InstagramSnowflakeIDGenerator(node_id=123)
    for _ in range(10):
        snowflake_id = generator.generate_next_id()
        assert snowflake_id.node_id() == 123


@pytest.mark.usefixtures("frozen_time")
def test_generate_next_id_timestamp_increases(
    frozen_time: FrozenDateTimeFactory,
    instagram_generator: InstagramSnowflakeIDGenerator,
) -> None:
    id1 = instagram_generator.generate_next_id()
    frozen_time.tick(timedelta(milliseconds=2))  # Sleep for 2ms
    id2 = instagram_generator.generate_next_id()

    assert id1.timestamp_ms(epoch=1000000000000) + 2 == id2.timestamp_ms(epoch=1000000000000)


@pytest.mark.usefixtures("frozen_time")
def test_generate_next_id_epoch_affects_timestamp() -> None:
    """Verify that custom epoch affects timestamp calculation correctly."""
    epoch1 = 1000000000000  # Earlier epoch
    epoch2 = 1500000000000  # Later epoch (500,000 seconds later)

    gen1 = InstagramSnowflakeIDGenerator(node_id=0, epoch=epoch1)
    gen2 = InstagramSnowflakeIDGenerator(node_id=0, epoch=epoch2)

    id1 = gen1.generate_next_id()
    id2 = gen2.generate_next_id()

    # Extract raw timestamp components (time since epoch, not absolute time)
    # Using epoch=0 gives us the raw internal timestamp value
    raw_ts1 = id1.timestamp_ms(epoch=0)
    raw_ts2 = id2.timestamp_ms(epoch=0)

    # With later epoch, internal timestamp should be smaller
    # (less time elapsed since epoch2 than since epoch1)
    assert raw_ts2 < raw_ts1

    # When we add back the correct epoch, both should give the same result
    abs_ts1 = id1.timestamp_ms(epoch=epoch1)
    abs_ts2 = id2.timestamp_ms(epoch=epoch2)
    assert abs_ts1 == abs_ts2


@pytest.mark.usefixtures("frozen_time")
def test_generate_next_id_different_nodes_unique() -> None:
    """Verify that IDs from different nodes are unique."""
    gen1 = InstagramSnowflakeIDGenerator(node_id=1)
    gen2 = InstagramSnowflakeIDGenerator(node_id=2)
    gen3 = InstagramSnowflakeIDGenerator(node_id=3)

    ids = []
    for _ in range(100):
        ids.append(gen1.generate_next_id())
        ids.append(gen2.generate_next_id())
        ids.append(gen3.generate_next_id())

    # All 300 IDs should be unique
    assert len(ids) == len(set(ids)) == 300

    # Verify each generator maintains its node_id
    for i in range(100):
        assert ids[i * 3].node_id() == 1
        assert ids[i * 3 + 1].node_id() == 2
        assert ids[i * 3 + 2].node_id() == 3


# Sequence overflow tests
def test_generate_exactly_max_sequence_plus_one_ids_same_ms(
    frozen_time: FrozenDateTimeFactory,
    instagram_generator: InstagramSnowflakeIDGenerator,
) -> None:
    """Test generating exactly max_sequence + 1 (1024) IDs in the same millisecond."""
    # Generate 1024 IDs (sequences 0-1023)
    ids = [instagram_generator.generate_next_id() for _ in range(1024)]

    # All should have same timestamp
    timestamps = [id_.timestamp_ms(epoch=0) for id_ in ids]
    assert len(set(timestamps)) == 1

    # Sequences should be 0-1023
    sequences = [id_.sequence() for id_ in ids]
    assert sequences == list(range(1024))

    # Next one requires time advance
    frozen_time.tick(timedelta(milliseconds=1, microseconds=1))
    next_id = instagram_generator.generate_next_id()
    assert next_id.sequence() == 0


@pytest.mark.usefixtures("frozen_time")
def test_sequence_overflow_calls_wait_for_next_timestamp(
    instagram_generator: InstagramSnowflakeIDGenerator,
) -> None:
    """Test that _wait_for_next_timestamp is called when sequence overflows."""
    # Mock _wait_for_next_timestamp to return the next timestamp
    with mock.patch.object(
        instagram_generator,
        "_wait_for_next_timestamp",
        return_value=instagram_generator.get_current_timestamp() + 1,
    ) as mock_wait:
        # Generate 1024 IDs (sequences 0-1023) - should NOT trigger wait
        for i in range(1024):
            id_ = instagram_generator.generate_next_id()
            assert id_.sequence() == i

        # At this point, sequence is at max (1023) and will overflow on next call
        assert mock_wait.call_count == 0

        # Generate one more ID - should trigger wait
        next_timestamp_id = instagram_generator.generate_next_id()

        # Verify wait was called exactly once
        assert mock_wait.call_count == 1
        mock_wait.assert_called_once()

        # Sequence should reset to 0
        assert next_timestamp_id.sequence() == 0


# Thread safety tests
def test_generator_thread_safe_concurrent_generation(
    instagram_generator: InstagramSnowflakeIDGenerator,
) -> None:
    ids: list[InstagramSnowflakeID] = []

    def generate_ids() -> None:
        ids.extend(instagram_generator.generate_next_id() for _ in range(100))

    threads = [threading.Thread(target=generate_ids) for _ in range(10)]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    # All IDs should be unique
    assert len(ids) == len(set(ids)) == 1000


# Clock-related errors
def test_clock_moved_backwards_raises_error(
    frozen_time: FrozenDateTimeFactory,
    instagram_generator: InstagramSnowflakeIDGenerator,
) -> None:
    # Generate an ID
    instagram_generator.generate_next_id()

    # Move time backwards by 1ms
    frozen_time.tick(timedelta(milliseconds=-1))

    # Trying to generate should raise error
    with pytest.raises(LastGenerationTimestampIsGreaterError):
        instagram_generator.generate_next_id()


def test_max_timestamp_reached_raises_error() -> None:
    # Create a generator with epoch far in the past so current timestamp exceeds max
    # This should fail during initialization
    with (
        freeze_time(timedelta(milliseconds=1 << 41)),
        pytest.raises(MaxTimestampHasReachedError),
    ):
        InstagramSnowflakeIDGenerator(node_id=0, epoch=0)


def test_max_timestamp_reached_during_generation(instagram_generator: InstagramSnowflakeIDGenerator) -> None:
    with (
        freeze_time(timedelta(milliseconds=1 << 41)),
        pytest.raises(MaxTimestampHasReachedError),
    ):
        instagram_generator.generate_next_id()


# Timestamp tests
def test_get_current_timestamp_returns_int() -> None:
    """Verify that get_current_timestamp returns an integer."""
    timestamp = InstagramSnowflakeIDGenerator.get_current_timestamp()
    assert isinstance(timestamp, int)


def test_get_current_timestamp_monotonic_increase(
    frozen_time: FrozenDateTimeFactory,
) -> None:
    """Verify that timestamps increase monotonically."""
    ts1 = InstagramSnowflakeIDGenerator.get_current_timestamp()
    # Tick forward
    frozen_time.tick(timedelta(milliseconds=2))
    ts2 = InstagramSnowflakeIDGenerator.get_current_timestamp()

    assert ts2 > ts1


def test_get_current_timestamp_resolution_1ms(
    frozen_time: FrozenDateTimeFactory,
) -> None:
    """Verify that Instagram generator has 1ms resolution."""
    ts1 = InstagramSnowflakeIDGenerator.get_current_timestamp()

    # Move time forward by exactly 2ms
    frozen_time.tick(timedelta(milliseconds=2))

    ts2 = InstagramSnowflakeIDGenerator.get_current_timestamp()

    # Difference should be exactly 2ms
    assert ts2 - ts1 == 2
