import logging
import sys
from collections import defaultdict

from rich import print as rprint

import bashautodoc.helpo.hfile as hfile
from bashautodoc.helpo.hsubprocess import run_cmd_with_output
from bashautodoc.models.filepath_datahandler import FilepathDatahandler
from bashautodoc.models.rst2md_datahandler import rst2md_mainroutine

# from bashautodoc.rst_and_md2md_file_writer import RstandM2MdFileWriter

LOG = logging.getLogger(__name__)


class CreateHandwrittenDocs:
    def __init__(self, conf, handwritten_docs_dir) -> None:
        self.conf = conf
        self.handwritten_docs_dir = handwritten_docs_dir
        self.handwritten_docs_infiles = []

        self.catname_2mdfile_dict = defaultdict(list)

        rprint("handwritten_docs_dir", self.handwritten_docs_dir)
        # sys.exit(42)
        # self.rst_files = []

    def convert_rst2md(self):
        """
        Convert rst files to md files.
        """

        rst2myst_configfile = self.conf.get("rst2myst_configfile")

        rst_glob = "{,**/}*.rst"
        myst_comm = (
            f"bash -O extglob -c 'rst2myst convert --replace-files --config {rst2myst_configfile} {self.handwritten_docs_dir}/"
            + rst_glob
            + "'"
        )
        run_cmd_with_output(comm_str=myst_comm)

    def create_hwdocs(self):
        import os

        # get the current working directory
        current_working_directory = os.getcwd()

        # print output to the console
        print(current_working_directory)
        self.convert_rst2md()

        rst2md_mainroutine()

        ##################################################
        hwdocs_infiles = hfile.search_directory_with_multiple_globs(
            search_path=self.handwritten_docs_dir,
            glob_patt_list=["*.md"],
        )

        self.handwritten_docs_infiles.extend(hwdocs_infiles)
        LOG.debug("handwritten_docs_infiles: %s", self.handwritten_docs_infiles)

        ##################################################

        # sys.exit(42)

        for docfile_rpath in self.handwritten_docs_infiles:
            docdata = FilepathDatahandler(
                infile_rpath=docfile_rpath,
                glob_patterns=self.conf.get("docs_glob_patterns"),
                replace_str=".md",
                category_names=self.conf.get("catnames_docs"),
                undef_category_dir=self.conf.get("undef_category_dir_hwdocs"),
                is_undef=None,
                leave_original_dir_structure=True,
            )

            # hfile.move_file(
            #     source=docdata.infile_rpath,
            #     target=docdata.outfile_rpath,
            # )

            # if "contributing" in docdata.outfile_rpath:
            #     rprint("docdata", docdata)

            #     ##################################################
            #     # rst_and_md2_md_file_writer = RstandM2MdFileWriter(
            #     #     conf=self.conf,
            #     #     docdata=docdata,
            #     # )
            #     # rst_and_md2_md_file_writer.process_hwdocs()
            #     sys.exit(42)

            ##################################################
            self.catname_2mdfile_dict[docdata.outfile_catname].append(
                docdata.outfile_rpath
            )
        return self.catname_2mdfile_dict
