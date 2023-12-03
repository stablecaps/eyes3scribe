"""Gen-Bash-MkDoc main entrypoint"""

import sys
import logging
import argparse
from autodocumatix.shell_2md_file_writer import Sh2MdFileWriter
from autodocumatix.helpo.hfile import mkdir_if_notexists
from autodocumatix.helpo.hstrops import false_when_str_contains_pattern

from autodocumatix.function_dependency_processor import FunctionDependencyProcessor
from rich import print as print

LOG = logging.getLogger(__name__)


class ShellSrcPreProcessor:
    def __init__(self, infiles, out_dir, exclude_patterns, debug=False):
        self.infiles = infiles
        self.out_dir = out_dir
        self.exclude_patterns = exclude_patterns
        self.debug = debug

        ###
        self.cleaned_infiles = self.clean_infiles()

        mkdir_if_notexists(target=self.out_dir)

    def dprint(self, myvar):
        if self.debug:
            print(f"{myvar = }")
            print("👉", locals())

    def clean_infiles(self):
        cleaned_infiles = [
            infile
            for infile in self.infiles
            if false_when_str_contains_pattern(
                test_str=infile, input_patt_li=self.exclude_patterns
            )
        ]
        return cleaned_infiles

    @staticmethod
    def get_function_name(line_str):
        func_name = None
        if line_str.strip().endswith(("{", "}")):
            # print("line:", line)

            function_header = line_str.split()
            func_name = function_header[1].strip("()")
            print("func_name:", func_name)
        return func_name

    def create_func_text_dict(self, infile_path):
        # 1. get names of all functions in file
        func_name_list = []
        full_alias_str_list = []
        func_name = None
        cite_about = "Undefined. Add composure cite-about to shell script file"

        with open(infile_path, "r") as FHI:
            self.dprint(infile_path)

            func_text_dict = {}
            src_text = FHI.read()

            for line in src_text.split("\n"):
                if line.startswith("function"):
                    func_name = self._process_function_line(
                        line, func_name_list, func_text_dict
                    )
                elif line.startswith(
                    (
                        "about-plugin",
                        "about-alias",
                        "about-completion",
                        "about-module",
                        "about-internal",
                    )
                ):
                    cite_about = self._process_about_line(line)
                elif line.startswith("alias"):
                    full_alias_str_list.append(self._process_alias_line(line))
                else:
                    if func_name is not None:
                        func_text_dict[func_name] += "\n" + line

        return func_name_list, full_alias_str_list, cite_about, func_text_dict

    def _process_function_line(self, line, func_name_list, func_text_dict):
        func_name = ShellSrcPreProcessor.get_function_name(line)
        if func_name is not None:
            func_name_list.append(func_name)
            func_text_dict[func_name] = line
        return func_name

    def _process_about_line(self, line):
        return (
            line.replace("about-plugin", "")
            .replace("about-alias", "")
            .replace("about-completion", "")
            .replace("about-module", "")
            .replace("about-internal", "")
            .replace("'", "")
            .strip()
        )

    def _process_alias_line(self, line):
        alias_list = line.replace("alias ", "").strip().split("=", 1)
        self.dprint(alias_list)

        alias_name = alias_list[0]
        alias_cmd = alias_list[1]
        alias_comment = ""

        if "#" in alias_list[1]:
            alias_list_lvl2 = alias_list[1].split("#", 1)
            alias_cmd = alias_list_lvl2[0]
            alias_comment = alias_list_lvl2[1]

        return f"| **{alias_name}** | `{alias_cmd[1:-1]}` | {alias_comment}\n"

    def main_routine(self):
        for infile_path in self.cleaned_infiles:
            LOG.info("Create func_text_dict for file: %s", infile_path)
            (
                func_name_list,
                full_alias_str_list,
                cite_about,
                func_text_dict,
            ) = self.create_func_text_dict(infile_path=infile_path)

            LOG.info("Create func_dep_dict for file: %s", infile_path)
            function_dependency_processor = FunctionDependencyProcessor(
                func_name_list=func_name_list, func_text_dict=func_text_dict
            )
            func_dep_dict = function_dependency_processor.create_func_dep_dict()

            LOG.debug("func_dep_dict = %s", func_dep_dict)
            # print("func_name_list", func_name_list)
            # if len(func_dep_dict) > 1:
            #     sys.exit(42)

            LOG.info("Print function data in func_dep_dict")
            for func_name, called_funcs in func_dep_dict.items():
                print(func_name, len(called_funcs), called_funcs)

            LOG.info("Convert shell files to markdown files")
            Sh2MdFileWriter(
                cite_about=cite_about,
                func_text_dict=func_text_dict,
                func_dep_dict=func_dep_dict,
                full_alias_str_list=full_alias_str_list,
                src_file_path=infile_path,
                out_dir=self.out_dir,
            )


# if __name__ == "__main__":
#     help_banner = "????????????????????"

#     parser = argparse.ArgumentParser(
#         description="Gen-Bash-MkDoc",
#         usage="??????????????????????",
#     )

#     parser.add_argument(
#         "-i",
#         "--infiles",
#         dest="infiles",
#         help="Space seperated strings of Bash src code files",
#         type=str,
#         nargs="*",
#         default=None,
#         required=True,
#     )

#     parser.add_argument(
#         "-o",
#         "--out-dir",
#         dest="out_dir",
#         help="Output folder to which processed documentation is written to",
#         type=str,
#         default=None,
#         required=True,
#     )

#     parser.add_argument(
#         "-x",
#         "--exclude-files",
#         dest="exclude_patterns",
#         help="FList of space seperated file path patterns to exclude",
#         type=str,
#         nargs="*",
#         default=[],
#     )

#     args = parser.parse_args()

#     shell_src_preprocessor = ShellSrcPreProcessor(
#         args.infiles, args.out_dir, args.exclude_patterns
#     )

#     shell_src_preprocessor.main_routine()


# https://adamj.eu/tech/2021/10/08/tips-for-debugging-with-print/
