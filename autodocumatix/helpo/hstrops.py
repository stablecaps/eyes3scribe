"""String Ops Helpers module."""

import os
import sys
import logging
import errno

LOG = logging.getLogger(__name__)


def false_when_str_contains_pattern(test_str, input_patt_li):
    """
    Returns False when the test string contains any pattern from the list. Is case sensitive.

    Args:
        test_str (str): The string to test.
        input_patt_li (list): The list of patterns to check for.

    Returns:
        bool: False if the test string contains any pattern, True otherwise.

    Example:
        >>> false_when_str_contains_pattern("Hello, world!", ["world", "!"])
        False
    """
    for idx in range(len(input_patt_li)):
        cleaned_pattern = input_patt_li[idx].strip()
        input_patt_li[idx] = cleaned_pattern

    test_str_clean = test_str.strip()
    for pattern in input_patt_li:
        print("*", pattern, test_str_clean)
        if pattern in test_str_clean:
            return False
    return True


def false_when_str_starts_with_pattern(test_str, input_patt_li):
    """
    Returns False when the test string starts with any pattern from the list. . Is case sensitive.

    Args:
        test_str (str): The string to test.
        input_patt_li (list): The list of patterns to check for.

    Returns:
        bool: False if the test string starts with any pattern, True otherwise.

    Example:
        >>> false_when_str_starts_with_pattern("Hello, world!", ["Hell", "world"])
        False
    """
    for idx in range(len(input_patt_li)):
        cleaned_pattern = input_patt_li[idx].strip()
        input_patt_li[idx] = cleaned_pattern

    test_str_clean = test_str.strip()
    for pattern in input_patt_li:
        print("*", pattern, test_str_clean)
        if test_str_clean.startswith(pattern):
            return False
    return True


def rm_lines_starting_with(multiline_str, rm_patt_list):
    """
    Removes lines from a multiline string that start with any pattern from the list.

    Args:
        multiline_str (str): The multiline string to process.
        rm_patt_list (list): The list of patterns to check for.

    Returns:
        str: The processed multiline string.

    Example:
        >>> rm_lines_starting_with("Hello,\nworld!", ["Hell", "world"])
        "world!"
    """
    out_str = ""
    for line in multiline_str.split("\n"):
        if false_when_str_starts_with_pattern(line, rm_patt_list):
            out_str += f"{line}\n"

    return out_str
