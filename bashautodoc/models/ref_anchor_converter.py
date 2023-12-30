import logging
import re
import sys
from collections import defaultdict
from dataclasses import dataclass, field

from rich import print as rprint

import bashautodoc.helpo.hfile as hfile
import bashautodoc.helpo.hstrops as hstrops

# from bashautodoc.helpo.hstrops import search_list_4pattern
from bashautodoc.helpo.hsubprocess import run_cmd_with_output
from bashautodoc.models.filepath_datahandler import FilepathDatahandler
from bashautodoc.regex_patterns import *

LOG = logging.getLogger(__name__)


class RefAnchorConverter:
    def __init__(
        self,
        r2m,
        anchorlinks_verbose_dict_all,
        anchorlinks_quickmap_dict_all,
    ):
        self.r2m = r2m
        self.anchorlinks_verbose_dict_all = anchorlinks_verbose_dict_all
        self.anchorlinks_quickmap_dict_all = anchorlinks_quickmap_dict_all

    @staticmethod
    def extract_reflink_start(reflink_start_match):
        ref_title = reflink_start_match.group(2).strip()

        if reflink_start_match.group(3) is None:
            reflink_start_raw = ref_title
        else:
            reflink_start_raw = reflink_start_match.group(3)

        reflink_start = reflink_start_raw.replace("<", "").replace(">", "").strip()
        rprint("reflink_start", reflink_start)

        return reflink_start, ref_title

    def get_reflink_end_file(self, reflink_start, reflink_start_norm):
        reflink_end_file = self.anchorlinks_quickmap_dict_all.get(reflink_start_norm)
        if reflink_end_file is None:
            print(f"ERROR: reflink_start not found: {reflink_start}")
            print(
                "anchorlinks_quickmap_dict_all keys",
                self.anchorlinks_quickmap_dict_all.keys(),
            )
            sys.exit(42)

        return reflink_end_file

    @staticmethod
    def generate_md_end_link(hxhash_match, reflink_label):
        hxhash = hxhash_match.group(1)
        hxhash_title = hxhash_match.group(2)
        rprint("hxhash", hxhash)
        rprint("hxhash_title", hxhash_title)
        md_end_link = f'{hxhash} <a id="{reflink_label}></a> {hxhash_title}'

        return md_end_link

    def generate_ref_sub_tuplist(self):
        """
        Generates a list of tuples for ref substitution.

        Args:
            mdtext (str): The text with replaced table of contents links.
            ref_start_patt (re.Pattern): The compiled regular expression pattern for refs.
            toclinks_dict (dict): The dictionary of table of contents links.

        Returns:
            list: The list of tuples for ref sub.
        """

        ref_sub_tuplist = []
        for line in self.r2m.filetext.split("\n"):
            if "{ref}" in line:
                reflink_start_match = re.search(ref_start_patt, line)
                if reflink_start_match is not None:
                    rprint("reflink_start_match", reflink_start_match)

                    reflink_start, ref_title = self.extract_reflink_start(
                        reflink_start_match
                    )

                    reflink_start_norm = hstrops.normalise_key(mystr=reflink_start)
                    rprint("reflink_start_norm", reflink_start_norm)

                    reflink_end_file = self.get_reflink_end_file(
                        reflink_start, reflink_start_norm
                    )

                    for ref_data in self.anchorlinks_verbose_dict_all[reflink_end_file]:
                        rprint("ref_data", ref_data)
                        reflink_label, reflink_end_header = ref_data[0], ref_data[1]
                        if reflink_label == reflink_start_norm:
                            rprint("reflink_end_header", reflink_end_header)

                            reflink_end_file_relative = (
                                hfile.get_relative_path_between_files(
                                    end_filepath=reflink_end_file,
                                    start_filepath=self.r2m.hwdoc_rpath,
                                )
                            )
                            hxhash_match = re.search(hxhash_patt, reflink_end_header)
                            if hxhash_match is not None:
                                md_end_link = self.generate_md_end_link(
                                    hxhash_match, reflink_label
                                )

                                md_reflink = f"[{ref_title}]({reflink_end_file_relative}#{reflink_label})"
                                rprint("md_reflink", md_reflink)

                            ref_sub_tuplist.append((line, md_reflink))
                            break
        return ref_sub_tuplist

    def replace_refs_with_links(self, ref_sub_tuplist):
        """
        Replaces refs with links in the text with replaced table of contents links.

        Args:
            mdtext (str): The text with replaced table of contents links.
            ref_sub_tuplist (list): The list of tuples for ref sub.

        Returns:
            str: The text with refs replaced with links.
        """
        for rst_ref_string, md_reflink in ref_sub_tuplist:
            tmp_filetext = self.r2m.filetext
            self.r2m.filetext = tmp_filetext.replace(rst_ref_string, md_reflink)

    def main(self):
        ref_sub_tuplist = self.generate_ref_sub_tuplist()

        rprint("ref_sub_tuplist", ref_sub_tuplist)
        if len(ref_sub_tuplist) > 0:
            sys.exit(42)
        self.replace_refs_with_links(ref_sub_tuplist=ref_sub_tuplist)
        return self.r2m.filetext
