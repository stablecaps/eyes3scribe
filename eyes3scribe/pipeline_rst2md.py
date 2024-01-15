import logging
import sys

from rich import print as rprint

from eyes3scribe.helpo.hfile import multiglob_dir_search, write_string_2file
from eyes3scribe.helpo.hsubprocess import run_cmd_with_output
from eyes3scribe.models.rst2md_datahandler import Rst2MdConverter1Toc
from eyes3scribe.regex_patterns import *

#
from eyes3scribe.rst2md_converters.r2m_anchors_end_step1 import R2MAnchorsEndStep1
from eyes3scribe.rst2md_converters.r2m_anchors_start_step2 import R2MAnchorsStartStep2
from eyes3scribe.rst2md_converters.r2m_triple_colonic_bypass import (
    R2MTripleColonicBypass,
)

LOG = logging.getLogger(__name__)


class PipelineRst2Md:
    def __init__(self, cnf):
        self.cnf = cnf
        self.toclinks_map_all = {}
        self.r2m_list = []

        self.anchorend_detail_map_all = {}
        self.anchorend_fast_map_all = {}

    # TODO: convert this to run only with user supplied switch
    def convert_rst2md(self):
        """
        Convert rst files to mdfiles.
        """

        LOG.info("Converting rst files to mdfiles.\nThis may take a while...")
        rst2myst_configfile = self.cnf.get("rst2myst_configfile")
        print(self.cnf.handwritten_docs_outdir)

        rst_glob = "{,**/}*.rst"
        myst_comm = (
            f"bash -O extglob -c 'rst2myst convert --replace-files --config {rst2myst_configfile} {self.cnf.handwritten_docs_outdir}/"
            + rst_glob
            + "'"
        )

        rprint("myst_comm", myst_comm)
        rst_converted = run_cmd_with_output(comm_str=myst_comm)

        if not rst_converted:
            LOG.error("rst2myst conversion failed.")
            sys.exit(42)

    def run(self):
        self.convert_rst2md()

        hwdocs_infiles = multiglob_dir_search(
            search_path=self.cnf.handwritten_docs_outdir,
            glob_patt_list=["*.md"],
        )
        rprint("hwdocs_infiles", hwdocs_infiles)
        # sys.exit(42)

        ### For every rst file
        # 1. establish if it has a TOC
        # 2. convert rst toc lkinks to makrkdown links
        # 3. return a  Rst2MdDataHolder object with relevant data
        # 4. store the Rst2MdDataHolder object in a list
        # 5. convert {ref} links to markdown links

        for hwdoc_rpath in hwdocs_infiles:
            r2m = Rst2MdConverter1Toc(
                cnf=self.cnf,
                hwdoc_rpath=hwdoc_rpath,
            )

            self.toclinks_map_all.update(r2m.toclinks_map)

            r2m_v2 = R2MAnchorsEndStep1(r2m=r2m)

            self.anchorend_detail_map_all.update(r2m_v2.anchorend_detail_map)

            self.anchorend_fast_map_all.update(r2m_v2.anchorend_fast_map)
            self.r2m_list.append(r2m_v2)

            # if "proxy_support" in hwdoc_rpath:
            #     sys.exit(42)

        rprint("\ntoclinks_map_all:")
        for toclink_key, toclink_val in self.toclinks_map_all.items():
            print("   >>", toclink_key + ":\t", toclink_val)

        rprint("\nanchorend_detail_map_all:")
        for anchor_key, anchor_val in self.anchorend_detail_map_all.items():
            print("   >>", anchor_key + ":\t", anchor_val)

        rprint("\nanchorend_fast_map_all:")
        for qanchor_key, qanchor_val in self.anchorend_fast_map_all.items():
            print("   >>", qanchor_key + ":\t", qanchor_val)

        # sys.exit(42)
        ### Replace rst ref links with markdown links
        for r2m in self.r2m_list:
            rprint("r2m", r2m)
            r2m_v3 = R2MAnchorsStartStep2(
                r2m=r2m,
                anchorend_detail_map_all=self.anchorend_detail_map_all,
                anchorend_fast_map_all=self.anchorend_fast_map_all,
            )
            rprint("r2m_v3", r2m_v3)
            r2m_v4 = R2MTripleColonicBypass(r2m=r2m_v3)

            # if "themes-list/index" in r2m.hwdoc_rpath:
            #     rprint("r2m.filetext", r2m.filetext)
            #     sys.exit(42)
            write_string_2file(f"{r2m.hwdoc_root}/{r2m.hwdoc_name}", r2m_v4.filetext)
        # sys.exit(42)
