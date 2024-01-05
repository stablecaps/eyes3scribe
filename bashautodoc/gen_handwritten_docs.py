import logging
import sys

from rich import print as rprint

from bashautodoc.gen_navbar_dict import GenNavbarDict
from bashautodoc.helpo import hfile
from bashautodoc.helpo.hsubprocess import run_cmd_with_output
from bashautodoc.models.rst2md_datahandler import run
from bashautodoc.pipeline_rst2md import PipelineRst2Md

# from bashautodoc.rst_and_md2md_file_writer import RstandM2MdFileWriter

LOG = logging.getLogger(__name__)


class GenHandwrittenDocs:
    def __init__(self, cnf) -> None:
        self.cnf = cnf
        # self.cnf.handwritten_docs_dir = handwritten_docs_dir
        self.handwritten_docs_infiles = []

        # self.catname_2mdfile_dict = defaultdict(list)

        rprint("handwritten_docs_dir", self.cnf.handwritten_docs_dir)
        # sys.exit(42)
        # self.rst_files = []

    def gen_handwritten_docs(self):
        ### Convert existing rst files to markdown format
        if self.cnf.handwritten_docs_rst:
            # self.convert_rst2md()
            pipeline_rst2_md = PipelineRst2Md(cnf=self.cnf)
            pipeline_rst2_md.run()
            # rprint("hello2")
            # sys.exit(42)

        # run(cnf=self.cnf, hwdocs_search_path="./docs_bash-it/docs/docshw/")

        ##################################################
        hwdocs_infiles = hfile.multiglob_dir_search(
            search_path=self.cnf.handwritten_docs_dir,
            glob_patt_list=["*.md"],
        )

        self.handwritten_docs_infiles.extend(hwdocs_infiles)
        LOG.debug("handwritten_docs_infiles: %s", self.handwritten_docs_infiles)

        # sys.exit(42)
        table_of_contents_processor = GenNavbarDict(
            cnf=self.cnf,
            search_path="docs_bash-it/docs/docshw/",
        )
        navbar_cleaned_dict = table_of_contents_processor.main()
        return navbar_cleaned_dict
