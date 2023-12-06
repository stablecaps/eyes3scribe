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
        srcfile_path,
        project_docs_dir,
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
        self.srcfile_path = srcfile_path
        self.project_docs_dir = project_docs_dir

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

        self.main_write_md()

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

    # # TODO: change this function anme to make it more descriptive
    # def organise_mdfiles_2subdirs(self):
    #     """
    #     Organize markdown files into subdirectories.
    #     """
    #     # probably only does one level
    #     category_names = self.conf.get("category_names")

    #     srcfile_path_split = self.srcfile_path.split("/")
    #     LOG.debug("srcfile_path_split: %s", srcfile_path_split)

    #     LOG.debug("shell_glob_patterns: %s", self.conf.get("shell_glob_patterns"))

    #     mdoutfile_name = str_multi_replace(
    #         input_str=srcfile_path_split[-1],
    #         rm_patt_list=self.conf.get("shell_glob_patterns"),
    #         replace_str=".md",
    #     )
    #     LOG.debug("mdoutfile_name: %s", mdoutfile_name)

    #     srcfile_relpath = self.srcfile_path.replace(
    #         self.conf.get("project_docs_dir"), ""
    #     )
    #     LOG.debug("srcfile_relpath: %s", srcfile_relpath)

    #     mdoutfile_abspath = None
    #     for catname in category_names:
    #         if f"/{catname}/" in srcfile_relpath:
    #             # TODO: this is pointlessly inefficient - fix it
    #             catpath = self.project_docs_dir + "/" + catname
    #             mkdir_if_notexists(target=catpath)
    #             mdoutfile_abspath = catpath + "/" + mdoutfile_name
    #             LOG.debug("mdoutfile_abspath: %s", mdoutfile_abspath)
    #             # sys.exit(42)

    #             return mdoutfile_abspath

    #     ### rule to undef if not in category_names
    #     udef_path = self.project_docs_dir + "/" + "undef"
    #     mkdir_if_notexists(target=udef_path)

    #     return udef_path + "/" + mdoutfile_name

    def organize_markdown_files_into_subdirectories(self):
        """
        Organize markdown files into subdirectories.
        """
        srcfile_path_split = self.srcfile_path.split("/")

        mdoutfile_name = str_multi_replace(
            input_str=srcfile_path_split[-1],
            rm_patt_list=self.conf.get("shell_glob_patterns"),
            replace_str=".md",
        )

        srcfile_relpath = self.srcfile_path.replace(
            self.conf.get("project_docs_dir"), ""
        )
        LOG.debug("shell_glob_patterns: %s", self.conf.get("shell_glob_patterns"))
        LOG.debug("srcfile_path_split: %s", srcfile_path_split)
        LOG.debug("mdoutfile_name: %s", mdoutfile_name)
        LOG.debug("srcfile_relpath: %s", srcfile_relpath)

        # probably only does one level
        category_names = self.conf.get("category_names")
        mdoutfile_abspath = None
        for catname in category_names:
            if f"/{catname}/" in srcfile_relpath:
                # TODO: this is pointlessly inefficient - fix it
                catpath = f"{self.project_docs_dir}/{catname}"
                mkdir_if_notexists(target=catpath)
                mdoutfile_abspath = f"{catpath}/{mdoutfile_name}"
                LOG.debug("mdoutfile_abspath: %s", mdoutfile_abspath)
                # sys.exit(42)

                return mdoutfile_abspath

        ### rule to undef if not in category_names
        # TDOD: use Pathlib
        udef_path = self.project_docs_dir + "/" + "undef"
        mkdir_if_notexists(target=udef_path)

        return udef_path + "/" + mdoutfile_name

    def main_write_md(self):
        """
        Perform the main routine of writing markdown files.

        This routine organizes markdown files into subdirectories, processes
        functions and aliases, and writes out the markdown file.
        """

        mdoutfile_abspath = self.organize_markdown_files_into_subdirectories()

        if "/explain.plugin" in mdoutfile_abspath:
            print("func_text_dict = ", self.func_text_dict)
            print("func_dep_dict = ", self.func_dep_dict)
            print("full_alias_str_list = ", self.full_alias_str_list)

            # sys.exit(42)

        # if "/plugins/" in mdoutfile_abspath:
        #     print("mdoutfile_abspath = ", mdoutfile_abspath)
        #     print("func_text_dict = ", self.func_text_dict)
        #     print("func_dep_dict = ", self.func_dep_dict)
        #     print("full_alias_str_list = ", self.full_alias_str_list)
        #     sys.exit(42)

        self.mdFile = MdUtils(file_name=mdoutfile_abspath, title=self.cite_about)

        mdoutfile_relpath = self.srcfile_path.replace(
            self.conf.get("project_docs_dir"), ""
        )
        self.mdFile.new_paragraph(f"***(in {mdoutfile_relpath})***")

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
