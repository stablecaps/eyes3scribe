from eyes3scribe.helpo.hstrops import str_multi_replace

# def test_does_str_contain_pattern():
#     # Test when the string contains a pattern
#     assert does_str_contain_pattern("Hello, world", ["world", ""]) == False

#     # Test when the string does not contain any pattern
#     assert (
#         does_str_contain_pattern("Hello, world", ["Goodbye", "earth"]) == True
#     )

#     # Test when the string is empty
#     assert does_str_contain_pattern("", ["Hell", "world"]) == True

#     # Test when the pattern list is empty
#     assert does_str_contain_pattern("Hello, world", []) == True

#     # Test when the string and the pattern list are both empty
#     assert does_str_contain_pattern("", []) == True

#     # Test when the string contains a pattern after stripping leading spaces
#     assert does_str_contain_pattern("  Hello, world  ", ["world", ""]) == False

#     # Test when the string contains a pattern but has different casing
#     assert does_str_contain_pattern("hello, world", ["WORLD", ""]) == False


#     # Test when the pattern list contains a pattern with leading or trailing spaces
#     assert does_str_contain_pattern("Hello, world", [" world ", "  "]) == False
# def test_does_str_contain_pattern():
#     # Test when the string contains a pattern
#     assert (
#         does_str_contain_pattern("Hello, world", ["world", ""]) is False
#     ), "Failed when the string contains a pattern"

#     # Test when the string does not contain any pattern
#     assert (
#         does_str_contain_pattern("Hello, world", ["Goodbye", "earth"]) is True
#     ), "Failed when the string does not contain any pattern"

#     # Test when the string is empty
#     assert (
#         does_str_contain_pattern("", ["Hell", "world"]) is True
#     ), "Failed when the string is empty"

#     # Test when the pattern list is empty
#     assert (
#         does_str_contain_pattern("Hello, world", []) is True
#     ), "Failed when the pattern list is empty"

#     # Test when the string and the pattern list are both empty
#     assert (
#         does_str_contain_pattern("", []) is True
#     ), "Failed when the string and the pattern list are both empty"

#     # Test when the string contains a pattern after stripping leading spaces
#     assert (
#         does_str_contain_pattern("  Hello, world  ", ["world", ""]) is False
#     ), "Failed when the string contains a pattern after stripping leading spaces"

#     # Test when the string contains a pattern but has different casing
#     assert (
#         does_str_contain_pattern("hello, world", ["WORLD", ""]) is False
#     ), "Failed when the string contains a pattern but has different casing"

#     # Test when the pattern list contains a pattern with leading or trailing spaces
#     assert (
#         does_str_contain_pattern("Hello, world", [" world ", "  "]) is False
#     ), "Failed when the pattern list contains a pattern with leading or trailing spaces"


# def test_does_str_start_with_pattern():
#     # Test when the string starts with a pattern
#     assert (
#         does_str_start_with_pattern("Hello, world", ["Hell", "world"]) is False
#     ), "Failed when the string starts with a pattern"

#     # Test when the string does not start with any pattern
#     assert (
#         does_str_start_with_pattern("Hello, world", ["Goodbye", "earth"]) is True
#     ), "Failed when the string does not start with any pattern"

#     # Test when the string is empty
#     assert (
#         does_str_start_with_pattern("", ["Hell", "world"]) is True
#     ), "Failed when the string is empty"

#     # Test when the pattern list is empty
#     assert (
#         does_str_start_with_pattern("Hello, world", []) is True
#     ), "Failed when the pattern list is empty"

#     # Test when the string and the pattern list are both empty
#     assert (
#         does_str_start_with_pattern("", []) is True
#     ), "Failed when the string and the pattern list are both empty"

#     # Test when the string starts with a pattern after stripping leading spaces
#     assert (
#         does_str_start_with_pattern("  Hello, world", ["Hell", "world"]) is False
#     ), "Failed when the string starts with a pattern after stripping leading spaces"

#     # Test when the string starts with a pattern after stripping trailing spaces
#     assert (
#         does_str_start_with_pattern("Hello, world  ", ["Hell", "world"]) is False
#     ), "Failed when the string starts with a pattern after stripping trailing spaces"

#     # Test when the string starts with a pattern but has different casing
#     assert (
#         does_str_start_with_pattern("hello, world", ["Hell", "world"]) is True
#     ), "Failed when the string starts with a pattern but has different casing"

#     # Test when the pattern list contains a pattern with leading or trailing spaces
#     assert (
#         does_str_start_with_pattern("Hello, world", [" Hell", "world "]) is False
#     ), "Failed when the pattern list contains a pattern with leading or trailing spaces"


# def test_str_multi_replace():
#     # Test when the string contains multiple patterns
#     assert (
#         str_multi_replace("Hello, world", ["world", ""]) == "Hello, "
#     ), "Failed on multiple patterns"

#     # Test when the string does not contain any pattern
#     assert (
#         str_multi_replace("Hello, world", ["Goodbye", "earth"]) == "Hello, world"
#     ), "Failed when no pattern"

#     # Test when the string is empty
#     assert str_multi_replace("", ["Hell", "world"]) == "", "Failed on empty string"

#     # Test when the pattern list is empty
#     assert (
#         str_multi_replace("Hello, world", []) == "Hello, world"
#     ), "Failed on empty pattern list"

#     # Test when the string and the pattern list are both empty
#     assert str_multi_replace("", []) == "", "Failed on empty string and pattern list"

#     # Test when the string contains a pattern after stripping leading spaces
#     assert (
#         str_multi_replace("  Hello, world  ", ["world", ""]) == "  Hello,   "
#     ), "Failed on leading spaces"

#     # Test when the string contains a pattern but has different casing
#     assert (
#         str_multi_replace("hello, world", ["WORLD", ""]) == "hello, world"
#     ), "Failed on different casing"

#     # Test when the pattern list contains a pattern with leading or trailing spaces
#     assert (
#         str_multi_replace("Hello, world", [" world ", "  "]) == "Hello, world"
#     ), "Failed on pattern with spaces"


def test_str_multi_replace():
    # Test when the string contains multiple patterns
    assert (
        str_multi_replace("Hello, world!", ["world", "!"], "") == "Hello, "
    ), "Failed on multiple patterns"

    # Test when the string does not contain any pattern
    assert (
        str_multi_replace("Hello, world!", ["Goodbye", "earth"], "") == "Hello, world!"
    ), "Failed when no pattern"

    # Test when the string is empty
    assert str_multi_replace("", ["Hell", "world"], "") == "", "Failed on empty string"

    # Test when the pattern list is empty
    assert (
        str_multi_replace("Hello, world!", [], "") == "Hello, world!"
    ), "Failed on empty pattern list"

    # Test when the string and the pattern list are both empty
    assert (
        str_multi_replace("", [], "") == ""
    ), "Failed on empty string and pattern list"

    # Test when the string contains a pattern after stripping leading spaces
    assert (
        str_multi_replace("  Hello, world!  ", ["world", "!"], "") == "  Hello,   "
    ), "Failed on leading spaces"

    # Test when the string contains a pattern but has different casing
    assert (
        str_multi_replace("hello, world!", ["WORLD", "!"], "") == "hello, world"
    ), "Failed on different casing"

    # Test when the pattern list contains a pattern with leading or trailing spaces
    assert (
        str_multi_replace("Hello, world!", [" world ", " ! "], "") == "Hello, world!"
    ), "Failed on pattern with spaces"

    # Test when the string contains multiple patterns and a replacement string is specified
    assert (
        str_multi_replace("Hello, world!", ["world", "!"], "planet")
        == "Hello, planetplanet"
    ), "Failed on multiple patterns with replacement string"
