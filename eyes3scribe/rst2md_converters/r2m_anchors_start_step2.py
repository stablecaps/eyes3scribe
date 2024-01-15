import logging
import re
import sys

from rich import print as rprint

from eyes3scribe.helpo import hfile, hstrops
from eyes3scribe.regex_patterns import anchorstart_patt

LOG = logging.getLogger(__name__)


class R2MAnchorsStartStep2:
    def __new__(
        cls,
        r2m,
        anchorend_detail_map_all,
        anchorend_fast_map_all,
    ):
        cls.r2m = r2m
        cls.anchorend_detail_map_all = anchorend_detail_map_all
        cls.anchorend_fast_map_all = anchorend_fast_map_all

        return cls.process_anchorstart_links()

    @staticmethod
    def extract_anchorstart(anchorstart_rst_match):
        anchor_title = anchorstart_rst_match.group(2).strip()

        if anchorstart_rst_match.group(3) is None:
            anchorstart_raw = anchor_title
        else:
            anchorstart_raw = anchorstart_rst_match.group(3)

        anchorstart = anchorstart_raw.replace("<", "").replace(">", "").strip()
        rprint("anchorstart", anchorstart)

        return anchorstart, anchor_title

    @classmethod
    def get_anchorend_file(cls, anchorstart, anchorstart_normkey):
        anchorend_file = cls.anchorend_fast_map_all.get(anchorstart_normkey)
        if anchorend_file is None:
            print(f"ERROR: anchorstart key not found: {anchorstart}")
            print(
                "anchorend_fast_map_all keys",
                cls.anchorend_fast_map_all.keys(),
            )
            sys.exit(42)

        return anchorend_file

    @staticmethod
    def gen_anchorend_link(hxhash_match, anchorend_normkey):
        hxhash = hxhash_match.group(1)
        hxhash_title = hxhash_match.group(2)
        rprint("hxhash", hxhash)
        rprint("hxhash_title", hxhash_title)
        anchorend_link = f'{hxhash} <a id="{anchorend_normkey}></a> {hxhash_title}'

        return anchorend_link

    @classmethod
    def convert_anchorstart_rst2md(cls):
        anchorstart_replace_list = []
        for line in cls.r2m.filetext.split("\n"):
            if "{ref}" in line:
                anchorstart_rst_match = re.search(anchorstart_patt, line)
                if anchorstart_rst_match:
                    anchorstart_rst_match_str = anchorstart_rst_match.group(0)
                    # e.g. match='{ref}`Contribution Guidelines <contributing>`'>
                    rprint("anchorstart_rst_match", anchorstart_rst_match)
                    rprint("anchorstart_rst_match_str", anchorstart_rst_match_str)

                    # anchorend_rst_line = line

                    # "Contribution Guidelines", "contributing"
                    anchorstart, anchor_title = cls.extract_anchorstart(
                        anchorstart_rst_match
                    )

                    anchorstart_normkey = hstrops.norm_key(mystr=anchorstart)
                    rprint("anchorstart_normkey", anchorstart_normkey)

                    # "docs_bash-it/docs/docshw/contributing.md"
                    anchorend_file = cls.get_anchorend_file(
                        anchorstart, anchorstart_normkey
                    )
                    # sys.exit(42)

                    # anchorend_data (all) = docs_bash-it/docs/docshw/contributing.md:	 [['contributing', '# Contribution Guidelines'], ['contributingtheme', '## Themes'], ['addscreenshot', '## Adding a Screenshot']]
                    for anchorend_data in cls.anchorend_detail_map_all[anchorend_file]:
                        rprint("anchorend_data", anchorend_data)
                        anchorend_normkey, anchorend_header_line, _ = (
                            anchorend_data[0],
                            anchorend_data[1],
                            anchorend_data[2],
                        )
                        # e.g. anchorend_normkey, anchorend_header_line = ['contributing', '# Contribution Guidelines']
                        if anchorend_normkey == anchorstart_normkey:
                            rprint(
                                "Found anchorend_header_line!", anchorend_header_line
                            )

                            anchorend_rpath = hfile.get_relative_path_between_files(
                                end_filepath=anchorend_file,
                                start_filepath=cls.r2m.hwdoc_rpath,
                            )
                            rprint("anchorend_rpath", anchorend_rpath)
                            rprint("anchorend_normkey", anchorend_normkey)
                            rprint("anchorend_header_line", anchorend_header_line)
                            # if "{ref}`restart" in anchorstart_rst_match_str:
                            #     sys.exit(42)

                            # make "[Contribution Guidelines](./contributing.md#contribution-guidelines)"
                            anchorstart_link = f"[{anchor_title}]({anchorend_rpath}#{anchorend_normkey})"
                            as_replace_holder = [
                                anchorstart_rst_match_str,
                                anchorstart_link,
                            ]
                            anchorstart_replace_list.append(as_replace_holder)
                            break
        return anchorstart_replace_list

    @classmethod
    def replace_anchorstart_links(cls, anchorstart_replace_list):
        for anchorstart_rst_match_str, anchorstart_link in anchorstart_replace_list:
            tmp_filetext = cls.r2m.filetext
            # if "{ref}`restart" in anchorstart_rst_match_str:
            #     sys.exit(42)
            cls.r2m.filetext = tmp_filetext.replace(
                anchorstart_rst_match_str, anchorstart_link
            )

    @classmethod
    def process_anchorstart_links(cls):
        anchorstart_replace_list = cls.convert_anchorstart_rst2md()

        rprint("anchorstart_replace_list", anchorstart_replace_list)
        # if len(ref_sub_tuplist) > 0:
        #     sys.exit(42)
        cls.replace_anchorstart_links(anchorstart_replace_list=anchorstart_replace_list)
        return cls.r2m
