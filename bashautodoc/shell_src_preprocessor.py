"""
This module contains the ShellSrcPreProcessor class. This class is used for
preprocessing shell source files for documentation generation.

The ShellSrcPreProcessor class provides methods to:
- Extract function names
- Process function definitions
- Process "about" statements
- Process alias definitions from shell source files

It also provides a main routine to:
- Create function text dictionaries
- Process function dependencies
- Convert shell files to markdown files

Classes:
    ShellSrcPreProcessor: Preprocesses shell source files for documentation.
"""

import logging
import sys
from collections import defaultdict

from rich import print as print

from bashautodoc.function_dependency_processor import FunctionDependencyProcessor
from bashautodoc.shell_2md_file_writer import Sh2MdFileWriter

LOG = logging.getLogger(__name__)


class ShellSrcPreProcessor:
    """Preprocesses shell source files for documentation generation."""

    def __init__(self, conf, cleaned_srcfiles_relpaths, project_docs_dir, debug=False):
        """
        Initialize the ShellSrcPreProcessor.

        Args:
            conf (str): Configuration information.
            cleaned_srcfiles_relpaths (list): List of cleaned input file paths.
            project_docs_dir (str): Directory path for project documentation.
            debug (bool, optional): Enable debug mode. Defaults to False.

        Example:
            preprocessor = ShellSrcPreProcessor(conf="config",
                                                cleaned_srcfiles_relpaths=["file1", "file2"],
                                                project_docs_dir="docs/",
        """
        self.conf = conf
        self.cleaned_srcfiles_relpaths = cleaned_srcfiles_relpaths
        self.project_docs_dir = project_docs_dir
        self.debug = debug

        self.catname_2mdfile_dict = defaultdict(list)

    def dprint(self, myvar):
        """
        Print the value of a variable using rich if debug mode is enabled.

        Args:
            myvar: Variable to be printed.

        Example:
            preprocessor = ShellSrcPreProcessor(conf="config",
                                                cleaned_srcfiles_relpaths=["file1", "file2"],
                                                project_docs_dir="docs/",
                                                debug=True)
            preprocessor.dprint("Hello, World!")
        """
        if self.debug:
            print(f"{myvar = }")
            print("👉", locals())

    @staticmethod
    def get_function_name(line_str):
        """
        Extracts the function name from a line of shell script.

        Args:
            line_str (str): A line of shell script.

        Returns:
            str: The name of the function.

        Example:
            function_name = ShellSrcPreProcessor.get_function_name("function hello_world {")
        """
        func_name = None
        if line_str.strip().endswith(("{", "}")):
            function_header = line_str.split()
            func_name = function_header[1].strip("()")
            LOG.debug("func_name: %s", func_name)
        return func_name

    def create_func_text_dict(self, srcfile_relpath):
        """
        Create a dictionary of function names and their corresponding code.

        Args:
            srcfile_relpath (str): Path to the src file.

        Returns:
            tuple: Tuple containing function name list, alias string list,
                   about citation, and function text dictionary.

        Example:
            preprocessor = ShellSrcPreProcessor(conf="config",
                                                cleaned_srcfiles_relpaths=["file1", "file2"],
                                                project_docs_dir="docs/",
                                                debug=True)
            func_name_list, alias_str_list, cite_about, func_text_dict =
                preprocessor.create_func_text_dict("file1")
        """
        func_name_list = []
        full_alias_str_list = []
        func_name = None
        cite_about = "Undefined. Add composure cite-about to shell script file"

        with open(srcfile_relpath, "r") as FHI:
            LOG.debug("srcfile_relpath: %s", srcfile_relpath)

            func_text_dict = {}
            src_text = FHI.read()

            for line in src_text.split("\n"):
                if line.startswith("function"):
                    func_name = ShellSrcPreProcessor.get_function_name(line)
                    if func_name is not None:
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
                    cite_about = self._process_about_line(line)
                elif line.startswith("alias"):
                    alias_str = self._process_alias_line(line)
                    if alias_str is not None:
                        full_alias_str_list.append(alias_str)
                else:
                    if func_name is not None:
                        func_text_dict[func_name] += "\n" + line

        return func_name_list, full_alias_str_list, cite_about, func_text_dict

    def _process_about_line(self, line):
        """
        Process a line of code containing an "about" statement.

        Args:
            line (str): Line of code.

        Returns:
            str: Processed about statement.

        Example:
            preprocessor = ShellSrcPreProcessor(conf="config",
                                                cleaned_srcfiles_relpaths=["file1", "file2"],
                                                project_docs_dir="docs/",
                                                debug=True)
            about_statement = preprocessor._process_about_line("about-plugin 'This is a plugin'")
        """
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
        """
        Process a line of code containing an alias definition.

        Args:
            line (str): Line of code.

        Returns:
            str: Processed alias string.

        Example:
            preprocessor = ShellSrcPreProcessor(conf="config",
                                                cleaned_srcfiles_relpaths=["file1", "file2"],
                                                project_docs_dir="docs/",
                                                debug=True)
            alias_string = preprocessor._process_alias_line("alias ls='ls -l' # List files")
        """
        LOG.debug("line: %s", line)

        alias_list = line.replace("alias ", "").strip().split("=", 1)
        LOG.debug("alias_list: %s", alias_list)

        if len(alias_list) < 2:
            return None

        alias_name = alias_list[0]
        alias_cmd = alias_list[1]
        alias_comment = ""

        if "#" in alias_list[1]:
            alias_list_lvl2 = alias_list[1].split("#", 1)
            alias_cmd = alias_list_lvl2[0]
            alias_comment = alias_list_lvl2[1]

        return f"| **{alias_name}** | `{alias_cmd[1:-1]}` | {alias_comment}\n"

    def main_routine(self):
        """
        Perform the main routine of preprocessing shell source files.

        This routine creates function text dictionaries, processes function
        dependencies, and converts shell files to markdown files.

        Example:
            preprocessor = ShellSrcPreProcessor(conf="config",
                                                cleaned_srcfiles_relpaths=["file1", "file2"],
                                                project_docs_dir="docs/",
                                                debug=True)
            preprocessor.main_routine()
        """
        for srcfile_relpath in self.cleaned_srcfiles_relpaths:
            ### These are being processed on a file-by-file basis
            (
                func_name_list,
                full_alias_str_list,
                cite_about,
                func_text_dict,
            ) = self.create_func_text_dict(srcfile_relpath=srcfile_relpath)

            function_dependency_processor = FunctionDependencyProcessor(
                func_name_list=func_name_list, func_text_dict=func_text_dict
            )
            func_dep_dict = function_dependency_processor.create_func_dep_dict()

            sh2_md_file_writer = Sh2MdFileWriter(
                self.conf,
                cite_about=cite_about,
                func_text_dict=func_text_dict,
                func_dep_dict=func_dep_dict,
                full_alias_str_list=full_alias_str_list,
                srcfile_relpath=srcfile_relpath,
            )
            catname, mdoutfile_relpath = sh2_md_file_writer.main_write_md()

            self.catname_2mdfile_dict[catname].append(mdoutfile_relpath)
        return self.catname_2mdfile_dict
