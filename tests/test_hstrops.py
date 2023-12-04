import pytest

from autodocumatix.helpo.hstrops import (
    false_when_str_contains_pattern,
    false_when_str_starts_with_pattern,
)

# def test_false_when_str_contains_pattern():
#     # Test when the string contains a pattern
#     assert false_when_str_contains_pattern("Hello, world!", ["world", "!"]) == False

#     # Test when the string does not contain any pattern
#     assert (
#         false_when_str_contains_pattern("Hello, world!", ["Goodbye", "earth"]) == True
#     )

#     # Test when the string is empty
#     assert false_when_str_contains_pattern("", ["Hell", "world"]) == True

#     # Test when the pattern list is empty
#     assert false_when_str_contains_pattern("Hello, world!", []) == True

#     # Test when the string and the pattern list are both empty
#     assert false_when_str_contains_pattern("", []) == True

#     # Test when the string contains a pattern after stripping leading spaces
#     assert false_when_str_contains_pattern("  Hello, world!  ", ["world", "!"]) == False

#     # Test when the string contains a pattern but has different casing
#     assert false_when_str_contains_pattern("hello, world!", ["WORLD", "!"]) == False


#     # Test when the pattern list contains a pattern with leading or trailing spaces
#     assert false_when_str_contains_pattern("Hello, world!", [" world ", " ! "]) == False
def test_false_when_str_contains_pattern():
    # Test when the string contains a pattern
    assert (
        false_when_str_contains_pattern("Hello, world!", ["world", "!"]) == False
    ), "Failed when the string contains a pattern"

    # Test when the string does not contain any pattern
    assert (
        false_when_str_contains_pattern("Hello, world!", ["Goodbye", "earth"]) == True
    ), "Failed when the string does not contain any pattern"

    # Test when the string is empty
    assert (
        false_when_str_contains_pattern("", ["Hell", "world"]) == True
    ), "Failed when the string is empty"

    # Test when the pattern list is empty
    assert (
        false_when_str_contains_pattern("Hello, world!", []) == True
    ), "Failed when the pattern list is empty"

    # Test when the string and the pattern list are both empty
    assert (
        false_when_str_contains_pattern("", []) == True
    ), "Failed when the string and the pattern list are both empty"

    # Test when the string contains a pattern after stripping leading spaces
    assert (
        false_when_str_contains_pattern("  Hello, world!  ", ["world", "!"]) == False
    ), "Failed when the string contains a pattern after stripping leading spaces"

    # Test when the string contains a pattern but has different casing
    assert (
        false_when_str_contains_pattern("hello, world!", ["WORLD", "!"]) == False
    ), "Failed when the string contains a pattern but has different casing"

    # Test when the pattern list contains a pattern with leading or trailing spaces
    assert (
        false_when_str_contains_pattern("Hello, world!", [" world ", " ! "]) == False
    ), "Failed when the pattern list contains a pattern with leading or trailing spaces"


def test_false_when_str_starts_with_pattern():
    # Test when the string starts with a pattern
    assert (
        false_when_str_starts_with_pattern("Hello, world!", ["Hell", "world"]) == False
    ), "Failed when the string starts with a pattern"

    # Test when the string does not start with any pattern
    assert (
        false_when_str_starts_with_pattern("Hello, world!", ["Goodbye", "earth"])
        == True
    ), "Failed when the string does not start with any pattern"

    # Test when the string is empty
    assert (
        false_when_str_starts_with_pattern("", ["Hell", "world"]) == True
    ), "Failed when the string is empty"

    # Test when the pattern list is empty
    assert (
        false_when_str_starts_with_pattern("Hello, world!", []) == True
    ), "Failed when the pattern list is empty"

    # Test when the string and the pattern list are both empty
    assert (
        false_when_str_starts_with_pattern("", []) == True
    ), "Failed when the string and the pattern list are both empty"

    # Test when the string starts with a pattern after stripping leading spaces
    assert (
        false_when_str_starts_with_pattern("  Hello, world!", ["Hell", "world"])
        == False
    ), "Failed when the string starts with a pattern after stripping leading spaces"

    # Test when the string starts with a pattern after stripping trailing spaces
    assert (
        false_when_str_starts_with_pattern("Hello, world!  ", ["Hell", "world"])
        == False
    ), "Failed when the string starts with a pattern after stripping trailing spaces"

    # Test when the string starts with a pattern but has different casing
    assert (
        false_when_str_starts_with_pattern("hello, world!", ["Hell", "world"]) == True
    ), "Failed when the string starts with a pattern but has different casing"

    # Test when the pattern list contains a pattern with leading or trailing spaces
    assert (
        false_when_str_starts_with_pattern("Hello, world!", [" Hell", "world "])
        == False
    ), "Failed when the pattern list contains a pattern with leading or trailing spaces"
