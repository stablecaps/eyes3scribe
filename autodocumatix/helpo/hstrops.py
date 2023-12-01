"""String Ops Helpers module."""

import os
import sys
import logging
import errno

LOG = logging.getLogger(__name__)


def filter_false_if_str_in_pattern(input_patt_li, test_str):
    """
    Filters a list of patterns to check if any pattern is present in the given test string.

    Args:
        input_patt_li (list): A list of patterns to be checked.
        test_str (str): The string to check for the presence of patterns.

    Returns:
        bool: Returns False if any pattern is found in the test string, True otherwise.

    Example:
        >>> patterns = ['abc', '123', 'xyz']
        >>> test_string = 'abcde'
        >>> filter_false_if_str_in_pattern(patterns, test_string)
        False
    """

    for pattern in input_patt_li:
        print("*", pattern, test_str)
        if pattern in test_str:
            return False
    return True


def rm_line_containing(multiline_str, rm_patt):
    """
    Removes lines containing a specified pattern from a multiline string.

    Args:
        multiline_str (str): The input multiline string containing multiple lines.
        rm_patt (str): The pattern to search for in each line and remove if found.

    Returns:
        str: A new multiline string with lines containing the specified pattern removed.

    Example:
        >>> input_str = "This is a test.\nLine to be removed.\nAnother line."
        >>> pattern_to_remove = "Line"
        >>> rm_line_containing(input_str, pattern_to_remove)
        'This is a test.\nAnother line.\n'
    """

    out_str = ""
    for line in multiline_str.split("\n"):
        if line.strip().startswith(rm_patt):
            pass
        else:
            out_str += f"{line}\n"
    return out_str
