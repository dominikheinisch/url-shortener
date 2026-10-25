import pytest

from shortener.codecs import (
    MAX_ID,
    InvalidShortCode,
    ShortCodeLimitReached,
    decode,
    encode,
)


@pytest.mark.parametrize(
    ("id_", "code"),
    [
        (0, "BAAAAA"),
        (1, "BAAAAB"),
        (2, "BAAAAC"),
        (63, "BAAAA_"),
        (64, "BAAABA"),
        (65, "BAAABB"),
        (100, "BAAABk"),
        (1_000, "BAAAPo"),
        (10_000, "BAACcQ"),
        (100_000, "BAAYag"),
        (MAX_ID - 1, "_____-"),
        (MAX_ID, "______"),
    ],
)
def test_encode_decode(id_: int, code: str) -> None:
    assert encode(id_) == code
    assert decode(code) == id_


def test_encode_raises_over_limit() -> None:
    with pytest.raises(ShortCodeLimitReached):
        encode(MAX_ID + 1)


def test_encode_raises_negative_id() -> None:
    with pytest.raises(ValueError):
        encode(-1)


@pytest.mark.parametrize("code", ["", "BAAAA", "BAAAAAA"])
def test_decode_raises_wrong_length(code: str) -> None:
    with pytest.raises(InvalidShortCode):
        decode(code)


@pytest.mark.parametrize("code", ["%5C%60", "BAAAA=", "BAAAA+", "BAAA A", "BAAAAé"])
def test_decode_raises_unknown_characters(code: str) -> None:
    with pytest.raises(InvalidShortCode):
        decode(code)


@pytest.mark.parametrize("code", ["AAAAAA", "AAAAAB", "A_____"])
def test_decode_raises_below_the_offset(code: str) -> None:
    with pytest.raises(InvalidShortCode):
        decode(code)
