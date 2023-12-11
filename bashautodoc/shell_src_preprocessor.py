"""
This module contains the ShellSrcPreProcessor class. This class is used for
preprocessing shell source files for documentation generation.

The ShellSrcPreProcessor class provides methods to:
- Extract function names
- Process function definitions
- Process "about" statements
- Process alias definitions from shell source files

It also provides a run routine to:
- Create function text dictionaries
- Process function dependencies
- Convert shell files to markdown files

Classes:
    ShellSrcPreProcessor: Preprocesses shell source files for documentation.
"""

import logging
import sys
from collections import defaultdict

from rich import print as rprint

from bashautodoc.function_dependency_processor import FunctionDependencyProcessor
from bashautodoc.models.filepath_datahandler import FilepathDatahandler
from bashautodoc.models.function_datahandler import FunctionDatahandler
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

        self.undef_category_dir = self.conf["undef_category_dir"]

        self.shell_glob_patterns = self.conf.get("shell_glob_patterns")
        self.catnames_src = self.conf.get("catnames_src")

        self.catname_2mdfile_dict = defaultdict(list)

    def run(self):
        """
        Perform the run routine of preprocessing shell source files.

        This routine creates function text dictionaries, processes function
        dependencies, and converts shell files to markdown files.

        Example:
            preprocessor = ShellSrcPreProcessor(conf="config",
                                                cleaned_srcfiles_relpaths=["file1", "file2"],
                                                project_docs_dir="docs/",
                                                debug=True)
            preprocessor.run()
        """
        for srcfile_relpath in self.cleaned_srcfiles_relpaths:
            ### These are being processed on a file-by-file basis

            funcdata = FunctionDatahandler(srcfile_relpath=srcfile_relpath)

            ##################################################
            is_undef = False
            func_text_dict_len = len(funcdata.func_text_dict)
            func_dep_dict_len = len(funcdata.func_dep_dict)
            full_alias_str_list_len = len(funcdata.full_alias_str_list)
            if (
                (func_text_dict_len == 0)
                and (func_dep_dict_len == 0)
                and (full_alias_str_list_len == 0)
            ):
                is_undef = True

            ##################################################
            srcdata = FilepathDatahandler(
                infile_relpath=srcfile_relpath,
                glob_patterns=self.conf.get("shell_glob_patterns"),
                replace_str=".md",
                category_names=self.catnames_src,
                undef_category_dir=self.undef_category_dir,
                is_undef=is_undef,
                leave_original_dir_structure=False,
            )

            # if "aliases" in srcdata.outfile_relpath:
            #     rprint("srcdata", srcdata)
            #     import sys

            #     sys.exit(42)

            ##################################################
            sh2_md_file_writer = Sh2MdFileWriter(
                conf=self.conf,
                funcdata=funcdata,
                srcdata=srcdata,
                srcfile_relpath=srcfile_relpath,
            )
            sh2_md_file_writer.write_md()

            ##################################################
            self.catname_2mdfile_dict[srcdata.outfile_catname].append(
                srcdata.outfile_relpath
            )
        return self.catname_2mdfile_dict
