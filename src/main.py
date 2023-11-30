"""Gen-Bash-MkDoc main entrypoint"""

import os
import sys
import logging
import argparse
from cite_parameter import CiteParameters
from helpers import mkdir_if_none, filter_false_if_str_in_pattern, rm_line_containing


LOG = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, stream=sys.stdout)


def clean_infiles(infile_list, exclude_patterns):
    cleaned_infiles = [
        infile
        for infile in infile_list
        if filter_false_if_str_in_pattern(
            input_patt_li=exclude_patterns, test_str=infile
        )
    ]
    return cleaned_infiles


def get_function_name(line_str):
    func_name = None
    if line_str.strip().endswith(("{", "}")):
        # print("line:", line)

        function_header = line_str.split()
        func_name = function_header[1].strip("()")
        print("func_name:", func_name)
    return func_name


def create_func_text_dict(infile_path):
    # 1. get names of all functions in file
    func_name_list = []
    full_alias_str_list = []
    func_name = None
    cite_about = "Undefined. Add composure cite-about to shell script file"
    with open(infile_path, "r") as FHI:
        print("infile_path", infile_path)

        func_text_dict = {}
        src_text = text = FHI.read()
        # print(src_text)
        for line in src_text.split("\n"):
            # print("ulu", line)

            if line.startswith("function"):
                func_name = get_function_name(line_str=line)
                if func_name is not None:  # and (len(func_text_dict) == 0):
                    # first function
                    func_name_list.append(func_name)
                    func_text_dict[func_name] = line
            elif line.startswith(
                (
                    "about-plugin",
                    "about-alias",
                    "about-completion",
                    "about-module",
                    "about-internal",
                )
            ):
                cite_about = (
                    line.replace("about-plugin", "")
                    .replace("about-alias", "")
                    .replace("about-completion", "")
                    .replace("about-module", "")
                    .replace("about-internal", "")
                    .replace("'", "")
                    .strip()
                )
            elif line.startswith("alias"):
                # pass alias into a container - write out full definition
                alias_list = line.replace("alias ", "").strip().split("=", 1)
                # print("alias_list", alias_list)

                alias_name = alias_list[0]
                alias_cmd = alias_list[1]
                alias_comment = ""
                # Further split alias line using "#" because final column is a description
                if "#" in alias_list[1]:
                    alias_list_lvl2 = alias_list[1].split("#", 1)
                    alias_cmd = alias_list_lvl2[0]
                    alias_comment = alias_list_lvl2[1]

                # if alias_name == "fgrep":
                #     print(
                #         "alias_name",
                #         "\n",
                #         alias_name,
                #         "\nd:",
                #         alias_cmd,
                #         "\nc:",
                #         alias_comment,
                #     )
                #     sys.exit(42)

                alias_fmtstr = (
                    f"| **{alias_name}** | `{alias_cmd[1:-1]}` | {alias_comment}\n"
                )

                full_alias_str_list.append(alias_fmtstr)

            else:
                if func_name is not None:
                    # func_name = func_name.strip("()")
                    func_text_dict[func_name] = func_text_dict[func_name] + "\n" + line
    return func_name_list, full_alias_str_list, cite_about, func_text_dict


def create_func_dep_dict(func_text_dict):
    func_dep_dict = {}
    print("func_name_list", func_name_list)
    print("func_text_dict", func_text_dict)
    for key, multiline_fdef in func_text_dict.items():
        cleaned_ml_fdef = rm_line_containing(multiline_str=multiline_fdef, rm_patt="#")
        print("\n*~~~~~yogi\n", key, "\n", cleaned_ml_fdef)
        for func_name in func_name_list:
            if func_name != key:  # exclude fuctions own name
                print("hoo1", key, func_name)
                if (func_name + " " in cleaned_ml_fdef) or (
                    "(" + func_name + ")" in cleaned_ml_fdef
                ):  # get wholeword function call  # search for function name in multiline function definition
                    if key not in func_dep_dict:
                        # create new entry
                        print("hoo2", func_name)
                        func_dep_dict[key] = [func_name]
                        # sys.exit(1)
                    else:
                        # append to exiting list
                        if func_name not in func_dep_dict[key]:  # unique values
                            func_dep_dict[key].append(func_name)

            # print(line)
    return func_dep_dict


# function_list = []

if __name__ == "__main__":
    help_banner = "????????????????????"

    parser = argparse.ArgumentParser(
        description="Gen-Bash-MkDoc",
        usage="??????????????????????",
    )

    parser.add_argument(
        "-i",
        "--infiles",
        dest="infiles",
        help="Space seperated strings of Bash src code files",
        type=str,
        nargs="*",
        default=None,
        required=True,
    )

    parser.add_argument(
        "-o",
        "--out-dir",
        dest="out_dir",
        help="Output folder to which processed documentation is written to",
        type=str,
        default=None,
        required=True,
    )

    parser.add_argument(
        "-x",
        "--exclude-files",
        dest="exclude_patterns",
        help="FList of space seperated file path patterns to exclude",
        type=str,
        nargs="*",
        default=[],
    )

    args = parser.parse_args()

    cleaned_infiles = clean_infiles(args.infiles, args.exclude_patterns)

    # print("cleaned_infiles", cleaned_infiles)
    # sys.exit(0)

    out_dir = args.out_dir
    mkdir_if_none(dir_name=out_dir)

    for infile_path in cleaned_infiles:
        print(infile_path)

        (
            func_name_list,
            full_alias_str_list,
            cite_about,
            func_text_dict,
        ) = create_func_text_dict(infile_path=infile_path)

        print("\n\n ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

        func_dep_dict = create_func_dep_dict(func_text_dict=func_text_dict)
        print("func_dep_dict", func_dep_dict)
        # sys.exit(1)

        print("\n\n ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        # from function_call_tree import draw_tree, parser

        for func_name, called_funcs in func_dep_dict.items():
            print("\nxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
            print("\n\n")

            print(func_name, len(called_funcs), called_funcs)
        #     print("\n")
        #     stringify_funccalls = func_name + ": " + " ".join(called_funcs) + "\n"

        #     for cfunc in called_funcs:
        #         if cfunc in func_dep_dict:
        #             # make a dependent string
        #             stringify_funccalls += (
        #                 cfunc + ": " + " ".join(func_dep_dict[cfunc]) + "\n"
        #             )
        #     print(f"\n{stringify_funccalls}")

        # draw_tree(parser(stringify_funccalls))

        # sys.exit(0)

        print("\n\n ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        # for key, value in func_text_dict.items():
        #     print("\n*~~~~~\n", key)  # , "\n", value)
        CiteParameters(
            cite_about=cite_about,
            func_text_dict=func_text_dict,
            func_dep_dict=func_dep_dict,
            full_alias_str_list=full_alias_str_list,
            src_file_path=infile_path,
            out_dir=out_dir,
        )
