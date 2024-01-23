"""String Ops Helpers module."""

import logging

from rich import print as rprint

LOG = logging.getLogger(__name__)


def get_lines_between_tags(filetext, start_tag="```{toctree}", end_tag="```"):
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


def get_lines_between_tag_and_blank_line(filetext, start_tag="```{toctree}"):
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


def get_multiblocks_between_tags(filetext, start_tag=":::", end_tag=":::"):
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
    return mystr.lower().replace(" ", "").replace("-", "").replace("_", "").strip()


def rreplace(mystr, match_str, replace_str, times):
    li = mystr.rsplit(match_str, times)
    return replace_str.join(li)


# TODO: find out what other functions can be generalised to simplify things
# TODO: move to collections helpers
def clean_list_via_rm_patts(input_list, rm_patt, rm_empty_lines=True):
    """
    Cleans the input list by rming lines that contain any of the rm_patts in the rm list.

    Args:
        input_list (list): The input list to clean.
        rm_patt (list): The list of rm_patts to rmude.
        rm_empty_lines (bool): Whether to rm empty lines.

    Returns:
        list: The clean list.
    """
    clean_list = []
    for line in input_list:
        line_is_empty = len(line.strip()) == 0
        line_contains_rm_patts = any(rm_patt in line for rm_patt in rm_patt)

        if line_is_empty and rm_empty_lines:
            continue
        if line_contains_rm_patts:
            continue

        clean_list.append(line)

    return clean_list


def does_str_contain_pattern(instr, input_patt_li):
    """
    Checks if a string contains any pattern from a list of patterns.

    Args:
        instr (str): The input string to check.
        input_patt_li (list): The list of patterns to search for.

    Returns:
        bool: True if any pattern is found in the input string, False otherwise.

    Example:
        contains_pattern = does_str_contain_pattern("Hello, world!", ["world", "!"])
    """

    instr_clean = instr.strip()
    for input_patt in input_patt_li:
        if input_patt.strip() in instr_clean:
            return True
    return False


def does_str_start_with_pattern(instr, input_patt_li):
    """
    Checks if a string starts with any pattern from a list of patterns.

    Args:
        instr (str): The input string to check.
        input_patt_li (list): The list of patterns to search for.

    Returns:
        bool: True if the input string starts with any pattern, False otherwise.

    Example:
        starts_with_pattern = does_str_start_with_pattern("Hello, world!", ["Hell", "world"])
    """
    for idx in range(len(input_patt_li)):
        clean_pattern = input_patt_li[idx].strip()
        input_patt_li[idx] = clean_pattern

    instr_clean = instr.strip()
    for pattern in input_patt_li:
        if instr_clean.startswith(pattern):
            return True
    return False


# TODO: use this function more
def multiline_str_2list(multiline_str, delimiter="\n"):
    mstr = multiline_str.split(delimiter)
    mstr_clean = [elem.strip() for elem in mstr if elem.strip() != ""]
    return mstr_clean


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

    multiline_str_list = multiline_str_2list(
        multiline_str=multiline_str, delimiter="\n"
    )
    print("multiline_str_list", multiline_str_list)
    filtered_multiline_str_list = [
        line
        for line in multiline_str_list
        if not does_str_start_with_pattern(line, rm_patt_list)
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


def clean_str_pline(instr, rm_patt):
    for rmpatt in rm_patt:
        instr = instr.replace(rmpatt, "")

    return instr.strip()


def replace_str_pline(instr, sub_tups):
    # use pipleine pattern [(targ1, rep1), (targ2, rep2), ..]
    for sub in sub_tups:
        instr = instr.replace(sub[0], sub[1])

    return instr.strip()


# TODO: remove all instances of this function - use replace_str_pline instead
def str_multi_replace(instr, rm_patt_list, replace_str):
    """
    Replace multiple substrings in the input string with a replacement string.

    Args:
        instr (str): The string to perform replacements on.
        rm_patt_list (list): A list of substrings to be replaced.
        replace_str (str, optional): The string to replace the substrings with.

    Returns:
        str: The input string with all specified substrings replaced with the replacement string.
    """
    for patt in rm_patt_list:
        patt_clean = patt.replace("*.", ".")
        print("patt_clean", patt_clean)
        instr = instr.replace(patt_clean, replace_str)
    return instr
