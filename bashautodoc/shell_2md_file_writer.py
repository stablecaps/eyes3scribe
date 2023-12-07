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

from bashautodoc.DocSectionWriterFunction import DocSectionWriterFunction
from bashautodoc.helpo.hfile import mkdir_if_notexists
from bashautodoc.helpo.hstrops import str_multi_replace

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
        self.udef_category_relpath = self.conf["udef_category_relpath"]

        self.shell_glob_patterns = self.conf.get("shell_glob_patterns")
        self.category_names = self.conf.get("category_names")

        self.sh2_md_file_writers = [
            "about",
            "group",
            "param",
            "example",
        ]

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
        srcfile_path_split = self.srcfile_relpath.split("/")
        srcfile_name = srcfile_path_split.pop()
        mdoutdir_relpath = "/".join(srcfile_path_split)

        mdoutfile_name = str_multi_replace(
            input_str=srcfile_name,
            rm_patt_list=self.conf.get("shell_glob_patterns"),
            replace_str=".md",
        )

        LOG.debug("shell_glob_patterns: %s", self.conf.get("shell_glob_patterns"))
        LOG.debug("srcfile_path_split: %s", srcfile_path_split)
        LOG.debug("mdoutdir_relpath: %s", mdoutdir_relpath)
        LOG.debug("mdoutfile_name: %s", mdoutfile_name)
        LOG.debug("srcfile_relpath: %s", self.srcfile_relpath)
        # sys.exit(42)

        # probably only does one level
        mdoutfile_relpath = None
        ######################################################
        ### If no functions or aliases, then send to undef so usert can fix
        func_text_dict_len = len(self.func_text_dict)
        func_dep_dict_len = len(self.func_dep_dict)
        full_alias_str_list_len = len(self.full_alias_str_list)
        if (
            (func_text_dict_len == 0)
            and (func_dep_dict_len == 0)
            and (full_alias_str_list_len == 0)
        ):
            return ("undef", f"{self.udef_category_relpath}/{mdoutfile_name}")

        ######################################################
        ### Check if category matches our desireted categories
        for catname in self.category_names:
            if catname in srcfile_path_split:
                # TODO: this is pointlessly inefficient - fix it
                catdir_relpath = f"{mdoutdir_relpath}/{catname}"
                mkdir_if_notexists(target=catdir_relpath)
                mdoutfile_relpath = f"{catdir_relpath}/{mdoutfile_name}"
                LOG.debug("mdoutfile_relpath: %s", mdoutfile_relpath)
                # sys.exit(42)

                return (catname, mdoutfile_relpath)

        ### rule to undef if not in category_names
        # TDOD: use Pathlib
        ###  Category not found or not wanted?
        return ("undef", f"{self.udef_category_relpath}/{mdoutfile_name}")

    def main_write_md(self):
        """
        Perform the main routine of writing markdown files.

        This routine organizes markdown files into subdirectories, processes
        functions and aliases, and writes out the markdown file.
        """

        catname, mdoutfile_relpath = self.sort_mdfiles_into_category_directories()

        # if "/explain.plugin" in mdoutfile_relpath:
        #     print("func_text_dict = ", self.func_text_dict)
        #     print("func_dep_dict = ", self.func_dep_dict)
        #     print("full_alias_str_list = ", self.full_alias_str_list)
        #     print("mdoutfile_relpath = ", mdoutfile_relpath)

        #     sys.exit(42)

        # if "/plugins/" in mdoutfile_relpath:
        #     print("mdoutfile_relpath = ", mdoutfile_relpath)
        #     print("func_text_dict = ", self.func_text_dict)
        #     print("func_dep_dict = ", self.func_dep_dict)
        #     print("full_alias_str_list = ", self.full_alias_str_list)
        #     sys.exit(42)

        self.mdFile = MdUtils(file_name=mdoutfile_relpath, title=self.cite_about)

        # mdoutfile_relpath = self.srcfile_relpath.replace(
        #     self.conf.get("project_docs_dir"), ""
        # )
        self.mdFile.new_paragraph(f"***(in {self.srcfile_relpath})***")

        ### Process functions
        if len(self.func_text_dict) > 0:
            doc_section_writer_function = DocSectionWriterFunction(
                mdFile=self.mdFile,
                func_text_dict=self.func_text_dict,
                func_dep_dict=self.func_dep_dict,
                cite_parameters=self.sh2_md_file_writers,
            )
            doc_section_writer_function.write_func_section()

        ### Process aliases
        if len(self.full_alias_str_list) > 0:
            self.write_aliases_section()

        ### Write out .md file
        self.mdFile.create_md_file()

        return (catname, mdoutfile_relpath)
