import binascii

import pytest

from snowflake_id_toolkit.instagram import InstagramSnowflakeID, InstagramSnowflakeIDGenerator


# Timestamp extraction tests
@pytest.mark.usefixtures("frozen_time")
def test_timestamp_ms_extraction_zero_epoch(instagram_id: InstagramSnowflakeID) -> None:
    # 2025-01-01 00:00:00 UTC = 1735689600000 ms
    assert instagram_id.timestamp_ms() == 1735689600000


@pytest.mark.usefixtures("frozen_time")
def test_timestamp_ms_extraction_custom_epoch() -> None:
    custom_epoch = 1609459200000  # 2021-01-01 00:00:00 UTC in ms
    generator = InstagramSnowflakeIDGenerator(node_id=0, epoch=custom_epoch)
    instagram_id = generator.generate_next_id()

    # Current time: 2025-01-01 00:00:00 UTC = 1735689600000 ms
    assert instagram_id.timestamp_ms(epoch=custom_epoch) == 1735689600000


# Component extraction tests
def test_node_id_extraction(instagram_id: InstagramSnowflakeID) -> None:
    assert instagram_id.node_id() == 0


def test_sequence_extraction(instagram_id: InstagramSnowflakeID) -> None:
    assert instagram_id.sequence() == 0


@pytest.mark.usefixtures("frozen_time")
def test_sequence_increments(instagram_generator: InstagramSnowflakeIDGenerator) -> None:
    id1 = instagram_generator.generate_next_id()
    id2 = instagram_generator.generate_next_id()

    assert id1.sequence() == 0
    assert id2.sequence() == 1


@pytest.mark.usefixtures("frozen_time")
def test_all_components_extraction() -> None:
    generator = InstagramSnowflakeIDGenerator(node_id=456)
    instagram_id = generator.generate_next_id()

    assert instagram_id.timestamp_ms() == 1735689600000
    assert instagram_id.node_id() == 456
    assert instagram_id.sequence() == 0


# Bytes encoding/decoding tests
def test_as_bytes_conversion(instagram_id: InstagramSnowflakeID) -> None:
    id_bytes = instagram_id.as_bytes()
    assert isinstance(id_bytes, bytes)
    assert len(id_bytes) == 8


def test_parse_bytes_roundtrip(instagram_id: InstagramSnowflakeID) -> None:
    id_bytes = instagram_id.as_bytes()
    parsed_id = InstagramSnowflakeID.parse_bytes(id_bytes)
    assert parsed_id == instagram_id


def test_parse_bytes_decoding() -> None:
    id_bytes = b"\x00\x00\x00\x00\x00\x00\x10\x00"
    parsed_id = InstagramSnowflakeID.parse_bytes(id_bytes)
    assert parsed_id == 4096


# Base16 encoding/decoding tests
def test_as_base16_encoding(instagram_id: InstagramSnowflakeID) -> None:
    base16 = instagram_id.as_base16()
    assert isinstance(base16, bytes)
    assert len(base16) == 16


def test_parse_base16_roundtrip(instagram_id: InstagramSnowflakeID) -> None:
    base16 = instagram_id.as_base16()
    parsed_id = InstagramSnowflakeID.parse_base16(base16)
    assert parsed_id == instagram_id


def test_parse_base16_decoding() -> None:
    base16 = b"0000000000001000"
    parsed_id = InstagramSnowflakeID.parse_base16(base16)
    assert parsed_id == 4096


def test_parse_base16_invalid_encoding() -> None:
    with pytest.raises(binascii.Error, match=r"Non-base16 digit found"):
        InstagramSnowflakeID.parse_base16(b"INVALID!")


# Base32 encoding/decoding tests
def test_as_base32_encoding(instagram_id: InstagramSnowflakeID) -> None:
    base32 = instagram_id.as_base32()
    assert isinstance(base32, bytes)


def test_parse_base32_roundtrip(instagram_id: InstagramSnowflakeID) -> None:
    base32 = instagram_id.as_base32()
    parsed_id = InstagramSnowflakeID.parse_base32(base32)
    assert parsed_id == instagram_id


def test_parse_base32_decoding() -> None:
    base32 = b"AAAAAAAAAAIAA==="
    parsed_id = InstagramSnowflakeID.parse_base32(base32)
    assert parsed_id == 4096


def test_parse_base32_invalid_encoding() -> None:
    with pytest.raises(binascii.Error, match=r"Non-base32 digit found"):
        InstagramSnowflakeID.parse_base32(b"INVALID!")


# Base64 encoding/decoding tests
def test_as_base64_encoding(instagram_id: InstagramSnowflakeID) -> None:
    base64 = instagram_id.as_base64()
    assert isinstance(base64, bytes)


def test_parse_base64_roundtrip(instagram_id: InstagramSnowflakeID) -> None:
    base64 = instagram_id.as_base64()
    parsed_id = InstagramSnowflakeID.parse_base64(base64)
    assert parsed_id == instagram_id


def test_parse_base64_decoding() -> None:
    base64 = b"AAAAAAAAEAA="
    parsed_id = InstagramSnowflakeID.parse_base64(base64)
    assert parsed_id == 4096


def test_parse_base64_invalid_encoding() -> None:
    with pytest.raises(binascii.Error, match="Incorrect padding"):
        InstagramSnowflakeID.parse_base64(b"INVALID!")


# Base64 URL-safe encoding/decoding tests
def test_as_base64_urlsafe_encoding(instagram_id: InstagramSnowflakeID) -> None:
    base64_urlsafe = instagram_id.as_base64_urlsafe()
    assert isinstance(base64_urlsafe, bytes)


def test_parse_base64_urlsafe_roundtrip(instagram_id: InstagramSnowflakeID) -> None:
    base64_urlsafe = instagram_id.as_base64_urlsafe()
    parsed_id = InstagramSnowflakeID.parse_base64_urlsafe(base64_urlsafe)
    assert parsed_id == instagram_id


def test_parse_base64_urlsafe_decoding() -> None:
    base64_urlsafe = b"AAAAAAAAEAA="
    parsed_id = InstagramSnowflakeID.parse_base64_urlsafe(base64_urlsafe)
    assert parsed_id == 4096


def test_parse_base64_urlsafe_invalid_encoding() -> None:
    with pytest.raises(binascii.Error, match="Incorrect padding"):
        InstagramSnowflakeID.parse_base64_urlsafe(b"INVALID!")


# Base85 encoding/decoding tests
def test_as_base85_encoding(instagram_id: InstagramSnowflakeID) -> None:
    base85 = instagram_id.as_base85()
    assert isinstance(base85, bytes)


def test_parse_base85_roundtrip(instagram_id: InstagramSnowflakeID) -> None:
    base85 = instagram_id.as_base85()
    parsed_id = InstagramSnowflakeID.parse_base85(base85)
    assert parsed_id == instagram_id


def test_parse_base85_decoding() -> None:
    base85 = b"00000000mG"
    parsed_id = InstagramSnowflakeID.parse_base85(base85)
    assert parsed_id == 4096


def test_parse_base85_invalid_encoding() -> None:
    with pytest.raises(ValueError, match=r"bad base85 character"):
        InstagramSnowflakeID.parse_base85("INVALID¡".encode())


# Integer behavior tests
@pytest.mark.usefixtures("frozen_time")
def test_id_behaves_as_int(instagram_id: InstagramSnowflakeID) -> None:
    assert isinstance(instagram_id, int)
    assert instagram_id == 14560019664076800000


@pytest.mark.usefixtures("frozen_time")
def test_comparison_operations(instagram_generator: InstagramSnowflakeIDGenerator) -> None:
    id1 = instagram_generator.generate_next_id()
    id2 = instagram_generator.generate_next_id()

    assert id1 < id2
    assert id2 > id1
    assert id1 == id1  # noqa: PLR0124
    assert id1 != id2


@pytest.mark.usefixtures("frozen_time")
def test_arithmetic_operations(instagram_id: InstagramSnowflakeID) -> None:
    result = instagram_id + 100
    assert result == 14560019664076800100
    assert result > instagram_id


# Edge cases
def test_id_zero_value() -> None:
    zero_id = InstagramSnowflakeID(0)
    assert zero_id == 0
    assert zero_id.timestamp_ms() == 0
    assert zero_id.node_id() == 0
    assert zero_id.sequence() == 0


def test_id_max_sequence_value() -> None:
    """Max sequence value for Instagram is 1023."""
    id_with_max_seq = InstagramSnowflakeID(1023)
    assert id_with_max_seq.sequence() == 1023
