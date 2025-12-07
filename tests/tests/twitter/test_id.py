import binascii

import pytest

from snowflake_id_toolkit.twitter import TwitterSnowflakeID, TwitterSnowflakeIDGenerator


# Timestamp extraction tests
@pytest.mark.usefixtures("frozen_time")
def test_timestamp_ms_extraction_zero_epoch(twitter_id: TwitterSnowflakeID) -> None:
    # 2025-01-01 00:00:00 UTC = 1735689600000 ms
    assert twitter_id.timestamp_ms() == 1735689600000


@pytest.mark.usefixtures("frozen_time")
def test_timestamp_ms_extraction_custom_epoch() -> None:
    custom_epoch = 1609459200000  # 2021-01-01 00:00:00 UTC in ms
    generator = TwitterSnowflakeIDGenerator(node_id=0, epoch=custom_epoch)
    twitter_id = generator.generate_next_id()

    # Current time: 2025-01-01 00:00:00 UTC = 1735689600000 ms
    assert twitter_id.timestamp_ms(epoch=custom_epoch) == 1735689600000


# Component extraction tests
def test_node_id_extraction(twitter_id: TwitterSnowflakeID) -> None:
    assert twitter_id.node_id() == 0


def test_sequence_extraction(twitter_id: TwitterSnowflakeID) -> None:
    assert twitter_id.sequence() == 0


@pytest.mark.usefixtures("frozen_time")
def test_all_components_extraction() -> None:
    generator = TwitterSnowflakeIDGenerator(node_id=123)
    twitter_id = generator.generate_next_id()

    assert twitter_id.timestamp_ms() == 1735689600000
    assert twitter_id.node_id() == 123
    assert twitter_id.sequence() == 0


# Bytes encoding/decoding tests
def test_as_bytes_conversion(twitter_id: TwitterSnowflakeID) -> None:
    id_bytes = twitter_id.as_bytes()
    assert isinstance(id_bytes, bytes)
    assert len(id_bytes) == 8


def test_parse_bytes_roundtrip(twitter_id: TwitterSnowflakeID) -> None:
    id_bytes = twitter_id.as_bytes()
    parsed_id = TwitterSnowflakeID.parse_bytes(id_bytes)
    assert parsed_id == twitter_id


def test_parse_bytes_decoding() -> None:
    id_bytes = b"\x00\x00\x00\x00\x00\x00\x10\x00"
    parsed_id = TwitterSnowflakeID.parse_bytes(id_bytes)
    assert parsed_id == 4096


# Base16 encoding/decoding tests
def test_as_base16_encoding(twitter_id: TwitterSnowflakeID) -> None:
    base16 = twitter_id.as_base16()
    assert isinstance(base16, bytes)
    assert len(base16) == 16


def test_parse_base16_roundtrip(twitter_id: TwitterSnowflakeID) -> None:
    base16 = twitter_id.as_base16()
    parsed_id = TwitterSnowflakeID.parse_base16(base16)
    assert parsed_id == twitter_id


def test_parse_base16_decoding() -> None:
    base16 = b"0000000000001000"
    parsed_id = TwitterSnowflakeID.parse_base16(base16)
    assert parsed_id == 4096


def test_parse_base16_invalid_encoding() -> None:
    with pytest.raises(binascii.Error, match=r"Non-base16 digit found"):
        TwitterSnowflakeID.parse_base16(b"INVALID!")


# Base32 encoding/decoding tests
def test_as_base32_encoding(twitter_id: TwitterSnowflakeID) -> None:
    base32 = twitter_id.as_base32()
    assert isinstance(base32, bytes)


def test_parse_base32_roundtrip(twitter_id: TwitterSnowflakeID) -> None:
    base32 = twitter_id.as_base32()
    parsed_id = TwitterSnowflakeID.parse_base32(base32)
    assert parsed_id == twitter_id


def test_parse_base32_decoding() -> None:
    base32 = b"AAAAAAAAAAIAA==="
    parsed_id = TwitterSnowflakeID.parse_base32(base32)
    assert parsed_id == 4096


def test_parse_base32_invalid_encoding() -> None:
    with pytest.raises(binascii.Error, match=r"Non-base32 digit found"):
        TwitterSnowflakeID.parse_base32(b"INVALID!")


# Base64 encoding/decoding tests
def test_as_base64_encoding(twitter_id: TwitterSnowflakeID) -> None:
    base64 = twitter_id.as_base64()
    assert isinstance(base64, bytes)


def test_parse_base64_roundtrip(twitter_id: TwitterSnowflakeID) -> None:
    base64 = twitter_id.as_base64()
    parsed_id = TwitterSnowflakeID.parse_base64(base64)
    assert parsed_id == twitter_id


def test_parse_base64_decoding() -> None:
    base64 = b"AAAAAAAAEAA="
    parsed_id = TwitterSnowflakeID.parse_base64(base64)
    assert parsed_id == 4096


def test_parse_base64_invalid_encoding() -> None:
    with pytest.raises(binascii.Error, match="Incorrect padding"):
        TwitterSnowflakeID.parse_base64(b"INVALID!")


# Base64 URL-safe encoding/decoding tests
def test_as_base64_urlsafe_encoding(twitter_id: TwitterSnowflakeID) -> None:
    base64_urlsafe = twitter_id.as_base64_urlsafe()
    assert isinstance(base64_urlsafe, bytes)


def test_parse_base64_urlsafe_roundtrip(twitter_id: TwitterSnowflakeID) -> None:
    base64_urlsafe = twitter_id.as_base64_urlsafe()
    parsed_id = TwitterSnowflakeID.parse_base64_urlsafe(base64_urlsafe)
    assert parsed_id == twitter_id


def test_parse_base64_urlsafe_decoding() -> None:
    base64_urlsafe = b"AAAAAAAAEAA="
    parsed_id = TwitterSnowflakeID.parse_base64_urlsafe(base64_urlsafe)
    assert parsed_id == 4096


def test_parse_base64_urlsafe_invalid_encoding() -> None:
    with pytest.raises(binascii.Error, match=r"Incorrect padding"):
        TwitterSnowflakeID.parse_base64_urlsafe(b"INVALID!")


# Base85 encoding/decoding tests
def test_as_base85_encoding(twitter_id: TwitterSnowflakeID) -> None:
    base85 = twitter_id.as_base85()
    assert isinstance(base85, bytes)


def test_parse_base85_roundtrip(twitter_id: TwitterSnowflakeID) -> None:
    base85 = twitter_id.as_base85()
    parsed_id = TwitterSnowflakeID.parse_base85(base85)
    assert parsed_id == twitter_id


def test_parse_base85_decoding() -> None:
    base85 = b"00000000mG"
    parsed_id = TwitterSnowflakeID.parse_base85(base85)
    assert parsed_id == 4096


def test_parse_base85_invalid_encoding() -> None:
    with pytest.raises(ValueError, match=r"bad base85 character"):
        TwitterSnowflakeID.parse_base85("INVALID¡".encode())


# Integer behavior tests
@pytest.mark.usefixtures("frozen_time")
def test_id_behaves_as_int(twitter_id: TwitterSnowflakeID) -> None:
    assert isinstance(twitter_id, int)
    assert twitter_id == 7280009832038400000


@pytest.mark.usefixtures("frozen_time")
def test_comparison_operations(twitter_generator: TwitterSnowflakeIDGenerator) -> None:
    id1 = twitter_generator.generate_next_id()
    id2 = twitter_generator.generate_next_id()

    assert id1 < id2
    assert id2 > id1
    assert id1 == id1  # noqa: PLR0124
    assert id1 != id2


@pytest.mark.usefixtures("frozen_time")
def test_arithmetic_operations(twitter_id: TwitterSnowflakeID) -> None:
    result = twitter_id + 100
    assert result == 7280009832038400100
    assert result > twitter_id


# Edge cases
def test_id_zero_value() -> None:
    zero_id = TwitterSnowflakeID(0)
    assert zero_id == 0
    assert zero_id.timestamp_ms() == 0
    assert zero_id.node_id() == 0
    assert zero_id.sequence() == 0


def test_id_max_sequence_value() -> None:
    """Max sequence value for Twitter is 4095."""
    id_with_max_seq = TwitterSnowflakeID(4095)
    assert id_with_max_seq.sequence() == 4095
