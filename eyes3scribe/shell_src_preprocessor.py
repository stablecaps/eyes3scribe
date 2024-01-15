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
from collections import defaultdict

from eyes3scribe.models.filepath_datahandler import FilepathDatahandler
from eyes3scribe.models.function_datahandler import FunctionDatahandler
from eyes3scribe.shell_2md_file_writer import Sh2MdFileWriter

LOG = logging.getLogger(__name__)


class ShellSrcPreProcessor:
    """Preprocesses shell source files for documentation generation."""

    def __init__(self, cnf, clean_srcfiles_rpaths, project_docs_dir, debug=False):
        """
        Initialize the ShellSrcPreProcessor.

        Args:
            cnf (str): Configuration information.
            clean_srcfiles_rpaths (list): List of clean input file paths.
            project_docs_dir (str): Directory path for project documentation.
            debug (bool, optional): Enable debug mode. Defaults to False.

        Example:
            preprocessor = ShellSrcPreProcessor(cnf="config",
                                                clean_srcfiles_rpaths=["file1", "file2"],
                                                project_docs_dir="docs/",
        """
        self.cnf = cnf
        self.clean_srcfiles_rpaths = clean_srcfiles_rpaths
        self.cnf.project_docs_dir = project_docs_dir
        self.debug = debug

        self.cnf.undef_category_dir = self.cnf["undef_category_dir"]

        self.cnf.shell_glob_patterns = self.cnf.get("shell_glob_patterns")
        self.catnames_src = self.cnf.get("catnames_src")

        self.catname_2mdfile_dict = defaultdict(list)

    def run(self):
        """
        Perform the run routine of preprocessing shell source files.

        This routine creates function text dictionaries, processes function
        dependencies, and converts shell files to markdown files.

        Example:
            preprocessor = ShellSrcPreProcessor(cnf="config",
                                                clean_srcfiles_rpaths=["file1", "file2"],
                                                project_docs_dir="docs/",
                                                debug=True)
            preprocessor.run()
        """
        for srcfile_rpath in self.clean_srcfiles_rpaths:
            ### These are being processed on a file-by-file basis

            funcdata = FunctionDatahandler(srcfile_rpath=srcfile_rpath)

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
                infile_rpath=srcfile_rpath,
                glob_patterns=self.cnf.get("shell_glob_patterns"),
                replace_str=".md",
                category_names=self.catnames_src,
                undef_category_dir=self.cnf.undef_category_dir,
                is_undef=is_undef,
                leave_original_dir_structure=False,
            )

            # if "aliases" in srcdata.outfile_rpath:
            #     rprint("srcdata", srcdata)
            #     import sys

            #     sys.exit(42)

            ##################################################
            sh2_md_file_writer = Sh2MdFileWriter(
                cnf=self.cnf,
                funcdata=funcdata,
                srcdata=srcdata,
                srcfile_rpath=srcfile_rpath,
            )
            sh2_md_file_writer.write_md()

            ##################################################
            self.catname_2mdfile_dict[srcdata.outfile_catname].append(
                srcdata.outfile_rpath
            )
        return self.catname_2mdfile_dict
