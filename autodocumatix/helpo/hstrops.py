"""String Ops Helpers module."""

import logging

LOG = logging.getLogger(__name__)


def false_when_str_contains_pattern(input_str, input_patt_li):
    """
    Returns False when the test string contains any pattern from the list. Is case sensitive.

    Args:
        input_str (str): The string to test.
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

    input_str_clean = input_str.strip()
    for pattern in input_patt_li:
        if pattern in input_str_clean:
            return False
    return True


def false_when_str_starts_with_pattern(input_str, input_patt_li):
    """
    Returns False when the test string starts with any pattern from the list. . Is case sensitive.

    Args:
        input_str (str): The string to test.
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

    input_str_clean = input_str.strip()
    for pattern in input_patt_li:
        if input_str_clean.startswith(pattern):
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


def str_multi_replace(input_str, rm_patt_list, replace_str):
    """
    Replace multiple substrings in the input string with a replacement string.

    Args:
        input_str (str): The string to perform replacements on.
        rm_patt_list (list): A list of substrings to be replaced.
        replace_str (str, optional): The string to replace the substrings with.

    Returns:
        str: The input string with all specified substrings replaced with the replacement string.
    """
    for patt in rm_patt_list:
        patt_cleaned = patt.replace("*.", ".")
        print("patt_cleaned", patt_cleaned)
        input_str = input_str.replace(patt_cleaned, replace_str)
    return input_str
