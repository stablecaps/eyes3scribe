"""
This module contains the Sh2MdFileWriter class which is responsible for
converting shell source files to markdown files for documentation.

The Sh2MdFileWriter class takes in configuration information, function text
and dependency dictionaries, a list of full alias strings, the source file path,
and the project documentation directory. It organizes markdown files into
subdirectories, processes functions and aliases, and writes out the markdown file.

Example:
    writer = Sh2MdFileWriter(conf="config",
                             cite_about="about citation",
                             func_text_dict={},
                             func_dep_dict={},
                             full_alias_str_list=[],
                             srcfile_path="file1",
                             project_docs_dir="docs/")
    writer.main_write_md()
"""
import logging
import os
import sys

from mdutils.mdutils import MdUtils
from rich import print as rprint

import bashautodoc.helpo.hfile as hfile
from bashautodoc.DocSectionWriterFunction import DocSectionWriterFunction
from bashautodoc.helpo.hfilepath_datahandler import FilepathDatahandler

# from bashautodoc.helpo.hstrops import str_multi_replace

LOG = logging.getLogger(__name__)


class Sh2MdFileWriter:
    """Converts shell source files to markdown files for documentation."""

    def __init__(
        self,
        conf,
        cite_about,
        func_text_dict,
        func_dep_dict,
        full_alias_str_list,
        srcfile_relpath,
    ):
        """
        Initialize the Shell2MdFileWriter.

        Args:
            conf (str): Configuration information.
            cite_about (str): About citation.
            func_text_dict (dict): Dictionary of function names and their code.
            func_dep_dict (dict): Dictionary of function dependencies.
            full_alias_str_list (list): List of full alias strings.
            srcfile_path (str): Path to the source file.
            project_docs_dir (str): Directory path for project documentation.

        Example:
            writer = Shell2MdFileWriter(conf="config",
                                        cite_about="about citation",
                                        func_text_dict={},
                                        func_dep_dict={},
                                        full_alias_str_list=[],
                                        srcfile_path="file1",
                                        project_docs_dir="docs/")
        """
        self.conf = conf
        self.cite_about = cite_about
        self.func_text_dict = func_text_dict
        self.func_dep_dict = func_dep_dict
        self.full_alias_str_list = full_alias_str_list
        self.srcfile_relpath = srcfile_relpath
        self.project_docs_dir = self.conf["project_docs_dir"]
        self.undef_category_dir = self.conf["undef_category_dir"]

        self.shell_glob_patterns = self.conf.get("shell_glob_patterns")
        self.catnames_src = self.conf.get("catnames_src")

        self.func_def_keywords = self.conf.get("func_def_keywords")
        # self.cparam_sort_mapper = {
        #     ">***about***": 0,
        #     ">***group***": 1,
        #     ">***param***": 2,
        #     ">***example***": 3,
        # }

    def write_aliases_section(self):
        """
        Write the aliases section to the markdown file.

        Example:
            writer = Shell2MdFileWriter(conf="config",
                                        cite_about="about citation",
                                        func_text_dict={},
                                        func_dep_dict={},
                                        full_alias_str_list=[],
                                        srcfile_path="file1",
                                        project_docs_dir="docs/")
            writer.write_aliases_section()
        """
        self.mdFile.new_header(
            level=2, title="Aliases", style="atx", add_table_of_contents="n"
        )

        mytable = ""
        mytable += "| **Alias Name** | **Code** | **Notes** |\n"
        mytable += "| ------------- | ------------- | ------------- |\n"
        for myalias in self.full_alias_str_list:
            mytable += myalias  # "| **" + ppass + "** | " + pp_dict[stack] + " |\n"

        self.mdFile.new_paragraph(mytable)

    def sort_mdfiles_into_category_directories(self):
        """
        Organize markdown files into subdirectories.
        """

        (
            srcfile_path_split,
            mdoutdir_relpath,
            mdoutfilename,
        ) = hfile.get_src_reldir_and_filename(
            file_relpath=self.srcfile_relpath,
            glob_patterns=self.conf.get("shell_glob_patterns"),
            replace_str=".md",
        )

        LOG.debug("srcfile_path_split: %s", srcfile_path_split)
        LOG.debug("mdoutdir_relpath: %s", mdoutdir_relpath)
        LOG.debug("mdoutfilename: %s", mdoutfilename)
        # sys.exit(42)

        # probably only does one level
        mdoutfile_relpath = None
        ######################################################
        ### If no functions or aliases, then send to undef so user can fix
        func_text_dict_len = len(self.func_text_dict)
        func_dep_dict_len = len(self.func_dep_dict)
        full_alias_str_list_len = len(self.full_alias_str_list)
        if (
            (func_text_dict_len == 0)
            and (func_dep_dict_len == 0)
            and (full_alias_str_list_len == 0)
        ):
            return ("undef", f"{self.undef_category_dir}/{mdoutfilename}")

        ######################################################
        ### Check if category matches our desired categories
        (
            catname,
            output_file_relpath,
        ) = hfile.get_categorydir_and_outfilepath(
            category_names=self.catnames_src,
            src_filepath_split=srcfile_path_split,
            outdir_relpath=mdoutdir_relpath,
            out_filename=mdoutfilename,
            undef_category_relpath=self.undef_category_dir,
        )

        return (
            catname,
            output_file_relpath,
        )

    def main_write_md(self):
        """
        Perform the main routine of writing markdown files.

        This routine organizes markdown files into subdirectories, processes
        functions and aliases, and writes out the markdown file.
        """

        # catname, mdoutfile_relpath = self.sort_mdfiles_into_category_directories()
        is_undef = False
        func_text_dict_len = len(self.func_text_dict)
        func_dep_dict_len = len(self.func_dep_dict)
        full_alias_str_list_len = len(self.full_alias_str_list)
        if (
            (func_text_dict_len == 0)
            and (func_dep_dict_len == 0)
            and (full_alias_str_list_len == 0)
        ):
            is_undef = True

        srcfile_data = FilepathDatahandler(
            infile_relpath=self.srcfile_relpath,
            glob_patterns=self.conf.get("shell_glob_patterns"),
            replace_str=".md",
            category_names=self.catnames_src,
            undef_category_dir=self.undef_category_dir,
            is_undef=is_undef,
        )

        # srcfile_data = fph.main()

        # LOG.debug("fph %s", fph)
        # LOG.debug("srcfile_data %s", srcfile_data)
        rprint("srcfile_data %s", srcfile_data)
        # if "autojump.plugin" in srcfile_data.outfile_relpath.lower():
        #     sys.exit(42)
        self.mdFile = MdUtils(
            file_name=srcfile_data.outfile_relpath, title=self.cite_about.capitalize()
        )

        self.mdFile.new_paragraph(f"***(in {self.srcfile_relpath})***")

        ### Process functions
        LOG.debug("self.func_def_keywords %s", self.func_def_keywords)

        if len(self.func_text_dict) > 0:
            doc_section_writer_function = DocSectionWriterFunction(
                mdFile=self.mdFile,
                func_text_dict=self.func_text_dict,
                func_dep_dict=self.func_dep_dict,
                cite_parameters=self.func_def_keywords,
            )
            doc_section_writer_function.write_func_section()

        ### Process aliases
        if len(self.full_alias_str_list) > 0:
            self.write_aliases_section()

        ### Write out .md file
        self.mdFile.create_md_file()

        # if "osx.plug" in mdoutfile_relpath.lower():
        #     sys.exit(42)

        return srcfile_data
