import logging
import re
import sys

from rich import print as rprint

from bashautodoc.helpo import hfile, hstrops
from bashautodoc.regex_patterns import hxhash_patt, ref_start_patt

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
    def generate_reflink_end(hxhash_match, reflink_label):
        hxhash = hxhash_match.group(1)
        hxhash_title = hxhash_match.group(2)
        rprint("hxhash", hxhash)
        rprint("hxhash_title", hxhash_title)
        reflink_end = f'{hxhash} <a id="{reflink_label}></a> {hxhash_title}'

        return reflink_end

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
                    # e.g. match='{ref}`Contribution Guidelines <contributing>`'>
                    rprint("reflink_start_match", reflink_start_match)

                    # "Contribution Guidelines", "contributing"
                    reflink_start, ref_title = self.extract_reflink_start(
                        reflink_start_match
                    )

                    reflink_start_norm = hstrops.normalise_key(mystr=reflink_start)
                    rprint("reflink_start_norm", reflink_start_norm)

                    # "docs_bash-it/docs/docshw/contributing.md"
                    reflink_end_file = self.get_reflink_end_file(
                        reflink_start, reflink_start_norm
                    )

                    # ref_data (all) = docs_bash-it/docs/docshw/contributing.md:	 [['contributing', '# Contribution Guidelines'], ['contributingtheme', '## Themes'], ['addscreenshot', '## Adding a Screenshot']]
                    for ref_data in self.anchorlinks_verbose_dict_all[reflink_end_file]:
                        rprint("ref_data", ref_data)
                        reflink_label, reflink_end_header = ref_data[0], ref_data[1]
                        # e.g. reflink_label, reflink_end_header = ['contributing', '# Contribution Guidelines']
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
                                # '#  <a id="contributing></a> Contribution Guidelines'
                                reflink_end = self.generate_reflink_end(
                                    hxhash_match, reflink_label
                                )

                                rprint("reflink_end", reflink_end)

                                ref_sub_tuplist.append((line, reflink_end))
                                break
        return ref_sub_tuplist

    def replace_refs_with_links(self, ref_sub_tuplist):
        # 1.
        for rst_ref_string, reflink_end in ref_sub_tuplist:
            tmp_filetext = self.r2m.filetext
            self.r2m.filetext = tmp_filetext.replace(rst_ref_string, reflink_end)

    def main(self):
        ref_sub_tuplist = self.generate_ref_sub_tuplist()

        rprint("ref_sub_tuplist", ref_sub_tuplist)
        if len(ref_sub_tuplist) > 0:
            sys.exit(42)
        self.replace_refs_with_links(ref_sub_tuplist=ref_sub_tuplist)
        return self.r2m.filetext
