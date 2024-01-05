"""
This module contains the Sh2MdFileWriter class which is responsible for
converting shell source files to markdown files for documentation.

The Sh2MdFileWriter class takes in configuration information, function text
and dependency dictionaries, a list of full alias strings, the source file path,
and the project documentation directory. It organizes markdown files into
subdirectories, processes functions and aliases, and writes out the markdown file.

Example:
    writer = Sh2MdFileWriter(cnf="config",
                             cite_about="about citation",
                             func_text_dict={},
                             func_dep_dict={},
                             full_alias_str_list=[],
                             srcfile_path="file1",
                             project_docs_dir="docs/")
    writer.write_md()
"""
import logging

from mdutils.mdutils import MdUtils
from rich import print as rprint

from bashautodoc.DocSectionWriterFunction import DocSectionWriterFunction

LOG = logging.getLogger(__name__)


class Sh2MdFileWriter:
    """Converts shell source files to markdown files for documentation."""

    def __init__(
        self,
        cnf,
        funcdata,
        srcdata,
        srcfile_rpath,
    ):
        """
        Initialize the Shell2MdFileWriter.

        Args:
            cnf (str): Configuration information.
            cite_about (str): About citation.
            func_text_dict (dict): Dictionary of function names and their code.
            func_dep_dict (dict): Dictionary of function dependencies.
            full_alias_str_list (list): List of full alias strings.
            srcfile_path (str): Path to the source file.
            project_docs_dir (str): Directory path for project documentation.

        Example:
            writer = Shell2MdFileWriter(cnf="config",
                                        cite_about="about citation",
                                        func_text_dict={},
                                        func_dep_dict={},
                                        full_alias_str_list=[],
                                        srcfile_path="file1",
                                        project_docs_dir="docs/")
        """
        self.cnf = cnf
        #
        self.cite_about = funcdata.cite_about
        self.func_text_dict = funcdata.func_text_dict
        self.func_dep_dict = funcdata.func_dep_dict
        self.full_alias_str_list = funcdata.full_alias_str_list
        #
        self.srcdata = srcdata
        #
        self.srcfile_rpath = srcfile_rpath

        self.cnf.project_docs_dir = self.cnf["project_docs_dir"]
        # self.cnf.undef_category_dir = self.cnf["undef_category_dir"]

        # self.cnf.shell_glob_patterns = self.cnf.get("shell_glob_patterns")
        # self.catnames_src = self.cnf.get("catnames_src")

        self.func_def_keywords = self.cnf.get("func_def_keywords")
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
            writer = Shell2MdFileWriter(cnf="config",
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

    def write_md(self):
        """
        Perform the main routine of writing markdown files.

        This routine organizes markdown files into subdirectories, processes
        functions and aliases, and writes out the markdown file.
        """

        rprint("srcdata %s", self.srcdata)
        # if "autojump.plugin" in srcdata.outfile_rpath.lower():
        #     sys.exit(42)
        self.mdFile = MdUtils(
            file_name=self.srcdata.outfile_rpath,
            title=self.cite_about.capitalize(),
        )

        self.mdFile.new_paragraph(f"***(in {self.srcfile_rpath})***")

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

        ### Write out .mdfile
        self.mdFile.create_md_file()
