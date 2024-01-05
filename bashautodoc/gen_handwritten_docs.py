import logging
import sys

from rich import print as rprint

from bashautodoc.helpo import hfile
from bashautodoc.helpo.hsubprocess import run_cmd_with_output
from bashautodoc.md_toc2_yaml_processor import MdToc2YamlProcessor
from bashautodoc.models.rst2md_datahandler import rst2md_mainroutine

# from bashautodoc.rst_and_md2md_file_writer import RstandM2MdFileWriter

LOG = logging.getLogger(__name__)


class GenHandwrittenDocs:
    def __init__(self, cnf, handwritten_docs_dir) -> None:
        self.cnf = cnf
        self.cnf.handwritten_docs_dir = handwritten_docs_dir
        self.handwritten_docs_infiles = []

        # self.catname_2mdfile_dict = defaultdict(list)

        rprint("handwritten_docs_dir", self.cnf.handwritten_docs_dir)
        # sys.exit(42)
        # self.rst_files = []

    def convert_rst2md(self):
        """
        Convert rst files to mdfiles.
        """

        LOG.info("Converting rst files to mdfiles.\nThis may take a while...")
        rst2myst_configfile = self.cnf.get("rst2myst_configfile")

        rst_glob = "{,**/}*.rst"
        myst_comm = (
            f"bash -O extglob -c 'rst2myst convert --replace-files --config {rst2myst_configfile} {self.cnf.handwritten_docs_dir}/"
            + rst_glob
            + "'"
        )
        run_cmd_with_output(comm_str=myst_comm)

    def gen_handwritten_docs(self):
        import os

        # get the current working directory
        current_working_directory = os.getcwd()

        ### Convert existing rst files to markdown format
        self.convert_rst2md()
        # sys.exit(42)

        rst2md_mainroutine(
            cnf=self.cnf, hwdocs_search_path="./docs_bash-it/docs/docshw/"
        )

        ##################################################
        hwdocs_infiles = hfile.multiglob_dir_search(
            search_path=self.cnf.handwritten_docs_dir,
            glob_patt_list=["*.md"],
        )

        self.handwritten_docs_infiles.extend(hwdocs_infiles)
        LOG.debug("handwritten_docs_infiles: %s", self.handwritten_docs_infiles)

        table_of_contents_processor = MdToc2YamlProcessor(
            cnf=self.cnf,
            search_path="docs_bash-it/docs/docshw/",
        )
        navbar_cleaned_dict = table_of_contents_processor.main()
        return navbar_cleaned_dict
