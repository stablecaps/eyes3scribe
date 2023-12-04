"""Class to extract composure cite parameters from function src code."""

import logging
import sys

from mdutils.mdutils import MdUtils

from autodocumatix.DocSectionWriterFunction import DocSectionWriterFunction
from autodocumatix.helpo.hfile import mkdir_if_notexists

LOG = logging.getLogger(__name__)


class Sh2MdFileWriter:
    def __init__(
        self,
        cite_about,
        func_text_dict,
        func_dep_dict,
        full_alias_str_list,
        src_file_path,
        project_docs_dir,
    ):
        self.cite_about = cite_about
        self.func_text_dict = func_text_dict
        self.func_dep_dict = func_dep_dict
        self.full_alias_str_list = full_alias_str_list
        self.src_file_path = src_file_path
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
        self.mdFile.new_header(
            level=2, title="Aliases", style="atx", add_table_of_contents="n"
        )

        mytable = ""
        mytable += "| **Alias Name** | **Code** | **Notes** |\n"
        mytable += "| ------------- | ------------- | ------------- |\n"
        for myalias in self.full_alias_str_list:
            mytable += myalias  # "| **" + ppass + "** | " + pp_dict[stack] + " |\n"

        self.mdFile.new_paragraph(mytable)

    def organise_mdfiles_2subdirs(self):
        # probably only does one level
        doc_cats = {
            "aliases": "aliases",
            "completion": "completion",
            "modules": "modules",
            "internal": "internal",
            "completions": "completions",
        }
        cat_substrings = list(doc_cats.keys())

        infile_path_name = self.src_file_path.split("/")
        LOG.debug("infile_path_name: %s", infile_path_name)

        outfile_name = infile_path_name[-1].replace(".sh", ".md")

        full_outfile_path = None
        for cat in cat_substrings:
            if cat in self.src_file_path:
                category = doc_cats.get(cat, None)
                outfile_path = self.project_docs_dir + "/" + category
                mkdir_if_notexists(target=outfile_path)
                full_outfile_path = outfile_path + "/" + outfile_name
                LOG.debug("full_outfile_path: %s", full_outfile_path)

                return full_outfile_path

        udef_path = self.project_docs_dir + "/" + "undef"
        mkdir_if_notexists(target=udef_path)
        return udef_path + "/" + outfile_name

        # sys.exit(0)

    def main_write_md(self):
        full_outfile_path = self.organise_mdfiles_2subdirs()

        self.mdFile = MdUtils(file_name=full_outfile_path, title=self.cite_about)
        self.mdFile.new_paragraph(f"***(in {self.src_file_path})***")

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
