import pytest
from day03 import has_neighbouring_symbol


@pytest.mark.parametrize(
    "lines, expected",
    [
        (["/..", "...", "..."], True),
        (["./.", "...", "..."], True),
        (["../", "...", "..."], True),
        (["...", "/..", "..."], True),
        (["...", "./.", "..."], False),
        (["...", "../", "..."], True),
        (["...", "...", "/.."], True),
        (["...", "...", "./."], True),
        (["...", "...", "../"], True),
    ],
)
def test_has_neighbouring_symbol(lines: list[str], expected: int):
    assert has_neighbouring_symbol(1, 1, lines) == expected
