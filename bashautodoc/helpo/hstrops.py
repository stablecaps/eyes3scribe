"""String Ops Helpers module."""

import logging

LOG = logging.getLogger(__name__)


def does_string_contain_pattern(input_str, input_patt_li):
    """
    Checks if a string contains any pattern from a list of patterns.

    Args:
        input_str (str): The input string to check.
        input_patt_li (list): The list of patterns to search for.

    Returns:
        bool: True if any pattern is found in the input string, False otherwise.

    Example:
        contains_pattern = does_string_contain_pattern("Hello, world!", ["world", "!"])
    """
    for idx in range(len(input_patt_li)):
        cleaned_pattern = input_patt_li[idx].strip()
        input_patt_li[idx] = cleaned_pattern

    input_str_clean = input_str.strip()
    for pattern in input_patt_li:
        if pattern in input_str_clean:
            return True
    return False


def does_string_starts_with_pattern(input_str, input_patt_li):
    """
    Checks if a string starts with any pattern from a list of patterns.

    Args:
        input_str (str): The input string to check.
        input_patt_li (list): The list of patterns to search for.

    Returns:
        bool: True if the input string starts with any pattern, False otherwise.

    Example:
        starts_with_pattern = does_string_starts_with_pattern("Hello, world!", ["Hell", "world"])
    """
    for idx in range(len(input_patt_li)):
        cleaned_pattern = input_patt_li[idx].strip()
        input_patt_li[idx] = cleaned_pattern

    input_str_clean = input_str.strip()
    for pattern in input_patt_li:
        if input_str_clean.startswith(pattern):
            return True
    return False


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
    multiline_str_list = multiline_str.split("\n")
    print("multiline_str_list", multiline_str_list)
    filtered_multiline_str_list = [
        line
        for line in multiline_str_list
        if not does_string_starts_with_pattern(line, rm_patt_list) and line != ""
    ]

    print("filtered_multiline_str_list", filtered_multiline_str_list)

    cleaned_outstr = "\n".join(filtered_multiline_str_list)
    print("cleaned_outstr", cleaned_outstr)

    # multiline_str_list_len = len(multiline_str_list)
    # idx = 0
    # for line in multiline_str_list:
    #     if does_string_starts_with_pattern(line, rm_patt_list):
    #         if idx == multiline_str_list_len - 1:
    #             out_str += f"{line}"
    #         else:
    #             out_str += f"{line}\n"
    #     idx += 1

    return cleaned_outstr


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
