import string

ALPHABET = string.ascii_uppercase + string.ascii_lowercase + string.digits + "-_"
BASE = len(ALPHABET)
CODE_LENGTH = 6
# Shifts every id into the 6-digit range, so ids 1..MAX_ID all get 6 characters.
OFFSET: int = BASE ** (CODE_LENGTH - 1)
MAX_ID: int = BASE**CODE_LENGTH - OFFSET - 1

_INDEX = {char: i for i, char in enumerate(ALPHABET)}


class ShortCodeLimitReached(ValueError):
    pass


class InvalidShortCode(ValueError):
    pass


def encode(id_: int) -> str:
    if id_ < 0:
        raise ValueError(f"id must not be negative, got {id_}")
    if id_ > MAX_ID:
        raise ShortCodeLimitReached(f"id {id_} is above the limit of {MAX_ID}")

    number = id_ + OFFSET
    chars = []
    while number:
        number, rest = divmod(number, BASE)
        chars.append(ALPHABET[rest])
    return "".join(reversed(chars))


def decode(code: str) -> int:
    if len(code) != CODE_LENGTH:
        raise InvalidShortCode(f"code must be {CODE_LENGTH} characters long")

    number = 0
    for char in code:
        if char not in _INDEX:
            raise InvalidShortCode(f"invalid character {char!r}")
        number = number * BASE + _INDEX[char]

    if number < OFFSET:
        raise InvalidShortCode("code is below the offset")
    return number - OFFSET
