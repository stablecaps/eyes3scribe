"""Gen-Bash-MkDoc main entrypoint"""

import logging
import sys

from rich import print as print

from autodocumatix.function_dependency_processor import FunctionDependencyProcessor
from autodocumatix.helpo.hfile import mkdir_if_notexists
from autodocumatix.helpo.hstrops import false_when_str_contains_pattern
from autodocumatix.shell_2md_file_writer import Sh2MdFileWriter

LOG = logging.getLogger(__name__)


class ShellSrcPreProcessor:
    def __init__(self, cleaned_infiles, project_docs_dir, debug=False):
        self.cleaned_infiles = cleaned_infiles
        self.project_docs_dir = project_docs_dir
        self.debug = debug

    def dprint(self, myvar):
        if self.debug:
            print(f"{myvar = }")
            print("👉", locals())

    @staticmethod
    def get_function_name(line_str):
        func_name = None
        if line_str.strip().endswith(("{", "}")):
            # print("line:", line)

            function_header = line_str.split()
            func_name = function_header[1].strip("()")
            LOG.debug("func_name: %s", func_name)
        return func_name

    def create_func_text_dict(self, infile_path):
        # 1. get names of all functions in file
        func_name_list = []
        full_alias_str_list = []
        func_name = None
        cite_about = "Undefined. Add composure cite-about to shell script file"

        with open(infile_path, "r") as FHI:
            LOG.debug("infile_path: %s", infile_path)

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
        LOG.debug("alias_list: %s", alias_list)

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
            # LOG.info("Create func_text_dict for file: %s", infile_path)
            (
                func_name_list,
                full_alias_str_list,
                cite_about,
                func_text_dict,
            ) = self.create_func_text_dict(infile_path=infile_path)

            # LOG.info("Create func_dep_dict for file: %s", infile_path)
            function_dependency_processor = FunctionDependencyProcessor(
                func_name_list=func_name_list, func_text_dict=func_text_dict
            )
            func_dep_dict = function_dependency_processor.create_func_dep_dict()

            # LOG.debug("func_dep_dict = %s", func_dep_dict)
            # print("func_name_list = ", func_name_list)
            # print("func_text_dict = ", func_text_dict)
            # if len(func_dep_dict) > 1:
            #     sys.exit(42)

            # LOG.info("Print function data in func_dep_dict")
            # for func_name, called_funcs in func_dep_dict.items():
            #     print(func_name, len(called_funcs), called_funcs)

            # LOG.info("Convert shell files to markdown files")
            Sh2MdFileWriter(
                cite_about=cite_about,
                func_text_dict=func_text_dict,
                func_dep_dict=func_dep_dict,
                full_alias_str_list=full_alias_str_list,
                src_file_path=infile_path,
                project_docs_dir=self.project_docs_dir,
            )
