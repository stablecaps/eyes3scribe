"""Helpers module."""

import os
import sys
import logging
import errno

LOG = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, stream=sys.stdout)


def mkdir_if_none(dir_name):
    """Create specified directory if it does not exist."""

    try:
        os.makedirs(dir_name)
    except OSError as err:
        if err.errno != errno.EEXIST:
            raise


def filter_false_if_str_in_pattern(input_patt_li, test_str):

    for pattern in input_patt_li:
        print("*", pattern, test_str)
        if pattern in test_str:
            return False
    return True


def rm_line_containing(multiline_str, rm_patt):
    out_str = ""
    for line in multiline_str.split("\n"):
        if line.strip().startswith(rm_patt):
            pass
        else:
            out_str += line + "\n"
    return out_str
