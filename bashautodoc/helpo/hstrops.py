"""String Ops Helpers module."""

import logging
import sys

from rich import print as rprint

LOG = logging.getLogger(__name__)


def does_str_contain_pattern(input_str, input_patt_li):
    """
    Checks if a string contains any pattern from a list of patterns.

    Args:
        input_str (str): The input string to check.
        input_patt_li (list): The list of patterns to search for.

    Returns:
        bool: True if any pattern is found in the input string, False otherwise.

    Example:
        contains_pattern = does_str_contain_pattern("Hello, world!", ["world", "!"])
    """
    for idx in range(len(input_patt_li)):
        clean_pattern = input_patt_li[idx].strip()
        input_patt_li[idx] = clean_pattern

    input_str_clean = input_str.strip()
    for pattern in input_patt_li:
        if pattern in input_str_clean:
            return True
    return False


def does_str_start_with_pattern(input_str, input_patt_li):
    """
    Checks if a string starts with any pattern from a list of patterns.

    Args:
        input_str (str): The input string to check.
        input_patt_li (list): The list of patterns to search for.

    Returns:
        bool: True if the input string starts with any pattern, False otherwise.

    Example:
        starts_with_pattern = does_str_start_with_pattern("Hello, world!", ["Hell", "world"])
    """
    for idx in range(len(input_patt_li)):
        clean_pattern = input_patt_li[idx].strip()
        input_patt_li[idx] = clean_pattern

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
        if not does_str_start_with_pattern(line, rm_patt_list) and line != ""
    ]

    print("filtered_multiline_str_list", filtered_multiline_str_list)

    clean_outstr = "\n".join(filtered_multiline_str_list)
    print("clean_outstr", clean_outstr)

    # multiline_str_list_len = len(multiline_str_list)
    # idx = 0
    # for line in multiline_str_list:
    #     if does_str_start_with_pattern(line, rm_patt_list):
    #         if idx == multiline_str_list_len - 1:
    #             out_str += f"{line}"
    #         else:
    #             out_str += f"{line}\n"
    #     idx += 1

    return clean_outstr


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
        patt_clean = patt.replace("*.", ".")
        print("patt_clean", patt_clean)
        input_str = input_str.replace(patt_clean, replace_str)
    return input_str


def extract_lines_between_tags(filetext, start_tag="```{toctree}", end_tag="```"):
    line_holder = []
    inRecordingMode = False
    for line in filetext.split("\n"):
        # line_stripped = line.strip()
        # TODO: this not in inRecordingMode is not easy to read
        if not inRecordingMode:
            if start_tag in line:
                rprint("TRUE: found toctree")
                inRecordingMode = True
                line_holder.append(line)
        elif end_tag in line:
            inRecordingMode = False
            line_holder.append(line)
        else:
            line_holder.append(line)

    return line_holder


def extract_lines_between_start_and_end_blank_line_tag(
    filetext, start_tag="```{toctree}"
):
    line_holder = []
    inRecordingMode = False
    for line in filetext.split("\n"):
        # line_stripped = line.strip()
        if not inRecordingMode:
            if start_tag in line:
                rprint("TRUE: found toctree")
                inRecordingMode = True
                line_holder.append(line)
        elif len(line) == 0:
            inRecordingMode = False
            line_holder.append(line)
        else:
            line_holder.append(line)

    return line_holder


def extract_multiblocks_between_start_and_end_line_tag(
    filetext, start_tag=":::", end_tag=":::"
):
    block_holder = []
    inRecordingMode = False
    for line in filetext.split("\n"):
        # rprint("line", line)
        # line_stripped = line.strip()
        if not inRecordingMode:
            if start_tag in line:
                # rprint("TRUE: found start_tag")
                inRecordingMode = True
                line_holder = []
                line_holder.append(line)
        elif end_tag in line:
            # rprint("TRUE: found end_tag")
            inRecordingMode = False
            line_holder.append(line)
            block_holder.append(line_holder)
        # elif inRecordingMode:
        else:
            line_holder.append(line)

    # rprint("block_holder", block_holder)
    # sys.exit(42)
    return block_holder


def norm_key(mystr):
    return mystr.lower().replace("-", "").replace("_", "").strip()


def rreplace(mystr, match_str, replace_str, times):
    li = mystr.rsplit(match_str, times)
    return replace_str.join(li)


# TODO: find out what other functions can be generalised to simplify things
def clean_list_via_rm_patts(input_list, rm_patterns, rm_empty_lines=True):
    """
    Cleans the input list by rming lines that contain any of the rm_patts in the rm list.

    Args:
        input_list (list): The input list to clean.
        rm_patterns (list): The list of rm_patts to rmude.
        rm_empty_lines (bool): Whether to rm empty lines.

    Returns:
        list: The clean list.
    """
    clean_list = []
    for line in input_list:
        line_is_empty = len(line.strip()) == 0
        line_contains_rm_patts = any(rm_patt in line for rm_patt in rm_patterns)

        if line_is_empty and rm_empty_lines:
            continue
        if line_contains_rm_patts:
            continue

        clean_list.append(line)

    return clean_list


# TODO: Create version that deals with custom replaecment strings
# use pipleine pattern [(targ1, rep1), (targ2, rep2), ..]
def clean_str_via_rm_patts(input_str, rm_patterns):
    for rmpatt in rm_patterns:
        input_str = input_str.replace(rmpatt, "")

    return input_str.strip()
