import logging

from rich import print as rprint

from eyes3scribe.gen_pynavbar_dict import GenPyNavbarDict
from eyes3scribe.pipeline_rst2md import PipelineRst2Md

LOG = logging.getLogger(__name__)


class GenHandwrittenDocs:
    def __init__(self, cnf) -> None:
        self.cnf = cnf
        # self.cnf.handwritten_docs_outdir = handwritten_docs_outdir
        self.handwritten_docs_infiles = []

        rprint("handwritten_docs_outdir", self.cnf.handwritten_docs_outdir)

    def gen_handwritten_docs(self):
        ### Convert existing rst files to markdown format
        if self.cnf.handwritten_docs_rst:
            pipeline_rst2_md = PipelineRst2Md(cnf=self.cnf)
            toclinks_map_all = pipeline_rst2_md.run()

        ##################################################


        # sys.exit(42)
        gen_py_navbar_dict = GenPyNavbarDict(
            cnf=self.cnf,
            search_path="docs_bash-it/docs/docshw/",
            toclinks_map_all=toclinks_map_all,
        )
        navbar_cleaned_dict = gen_py_navbar_dict.main()
        return navbar_cleaned_dict
