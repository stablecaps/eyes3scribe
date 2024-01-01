import copy
import logging
import re
import sys
from collections import defaultdict
from dataclasses import dataclass, field

from rich import print as rprint

from bashautodoc.helpo import hfile, hstrops
from bashautodoc.regex_patterns import anchorend_patt, anchorstart_patt, hxhash_patt

LOG = logging.getLogger(__name__)


class Rst2MdConverter2AnchorsEnd1:
    def __new__(
        cls,
        r2m,
    ):
        cls.r2m = r2m
        cls.r2m.anchorend_fast_map = {}

        return cls.process_anchorend_links()

    @staticmethod
    def gen_anchorend_link(hxhash_match, anchorend_normkey):
        hxhash = hxhash_match.group(1)
        hxhash_title = hxhash_match.group(2)
        rprint("hxhash", hxhash)
        rprint("hxhash_title", hxhash_title)
        anchorend_link = f'{hxhash} <a id="{anchorend_normkey}"></a> {hxhash_title}'

        return anchorend_link

    @classmethod
    def process_anchorend_links(cls):
        # 1. Search md text for anchorend_links in format "(help-screens)=".
        #   1.1. This is added to anchorend_header_replace_list so that it can be deleted as the
        #        mdlink will be to the next header.
        # 2. If true, search for next hx header. e.g. "## Help Screens".
        # 3. Construct anchorend_fast_map mapping {"helpscreens": "$filepath.md"}.
        #    Note: helpscreens is a normalised key.
        # 4. Construct anchorend_detail_map mapping {"$filepath.md": ["helpscreens", "## Help Screens"]}.
        # 5. Remove all rst anchor links from the md text.
        #   5.1. Later we will need to replace headers with the new syntax for anchorend_link. i.e.
        #        "#  <a id="helpscreens"></a> Help Screens".

        # We need to create a link from anchorstart --> anchorstart.
        # anchorstart_link = '[link](./contributing.md#contributing)'.
        # anchorend_link = '#  <a id="contributing></a> Contribution Guidelines'.
        # 1. Scan through any given mdfile and find all anchorstart_patts.
        #    e.g. match='{ref}`Contribution Guidelines <contributing>`'>.
        # 2. Create anchorend_link by:
        #     2.1. Find relative path to anchorend file (with respect to anchorstart file).
        #     2.2. Extract anchor_title and anchorstart. e.g. "Contribution Guidelines", "contributing".
        #     2.3. Find anchorend_filename from anchorend_fast_map.
        #     2.4. Use anchorend_filename to find "anchorend_normkey" &  "anchorend_header_line" from
        #          anchorend_detail_map. e.g. docs_bash-it/docs/docshw/contributing.md:
        #          [['contributing', '# Contribution Guidelines'], ['contributingtheme', '## Themes'],
        #           ['addscreenshot', '## Adding a Screenshot']].
        #     2.5. If (normalised) 1anchorend_normkey matches anchorstart_normkey we have a link match. Thus, if
        #           anchorstart_normkey is "contributing" the anchorend_normkey is "contributing" which means that
        #           we create a link to the header "## Contribution Guidelines" in the file "contributing.md".
        #     2.6. Create a link for anchorend e.g.
        #           '#  <a id="contributing></a> Contribution Guidelines'

        #     2.6. Create a link from anchorstart --> anchorstart. e.g.
        #          "[Contribution Guidelines](./contributing.md#contribution-guidelines)" -->
        #           '#  <a id="contributing></a> Contribution Guidelines'

        anchorend_rst_line_rm_list = []
        anchorend_header_replace_list = []
        is_next_line_header = False
        anchorend_key = None
        for line in cls.r2m.filetext.split("\n"):
            anchorend_rst_match = re.search(anchorend_patt, line)

            if anchorend_rst_match:
                anchorend_key = anchorend_rst_match.group(1)

                anchorend_rst_line = line
                anchorend_rst_line_rm_list.append(anchorend_rst_line)

                is_next_line_header = True

                rprint("anchorend_rst_line", anchorend_rst_line)
                rprint("anchorend_rst_match", anchorend_rst_match)
                rprint("is_next_line_header", is_next_line_header)
            elif is_next_line_header:
                if (
                    line.startswith("# ")
                    or line.startswith("## ")
                    or line.startswith("### ")
                    or line.startswith("#### ")
                ):
                    anchorend_header_line = line.strip()
                    rprint(
                        "anchorend_header_line",
                        anchorend_header_line,
                        is_next_line_header,
                    )

                    anchorend_normkey = hstrops.norm_key(
                        mystr=(anchorend_key.replace("(", "").replace(")=", "").strip())
                    )

                    hxhash_match = re.search(hxhash_patt, anchorend_header_line)
                    if hxhash_match:
                        # '#  <a id="contributing></a> Contribution Guidelines'
                        anchorend_link = Rst2MdConverter2AnchorsEnd1.gen_anchorend_link(
                            hxhash_match, anchorend_normkey
                        )
                        rprint("anchorend_link", anchorend_link)

                    ae_replace_holder = [anchorend_header_line, anchorend_link]
                    anchorend_header_replace_list.append(ae_replace_holder)

                    #
                    #
                    cls.r2m.anchorend_fast_map[anchorend_normkey] = cls.r2m.hwdoc_rpath
                    #
                    #
                    cls.r2m.anchorend_detail_map[cls.r2m.hwdoc_rpath].append(
                        [anchorend_normkey, anchorend_header_line, anchorend_link]
                    )
                    is_next_line_header = False

        ###################################################
        ### replace headers with anchorend_links
        print()
        for anchorend_header_line, anchorend_link in anchorend_header_replace_list:
            rprint(
                "anchorend_header_line, anchorend_link = ",
                anchorend_header_line + "x",
                anchorend_link,
            )
            tmp_filetext = copy.deepcopy(cls.r2m.filetext)
            cls.r2m.filetext = tmp_filetext.replace(
                anchorend_header_line, anchorend_link
            )

        ### remove rst anchorends
        print()
        for anchorend_rst_line in anchorend_rst_line_rm_list:
            rprint("anchorend_rst_line", anchorend_rst_line)
            tmp_filetext = copy.deepcopy(cls.r2m.filetext)
            cls.r2m.filetext = tmp_filetext.replace(anchorend_rst_line, "")
        return cls.r2m


class Rst2MdConverter2AnchorsStart2:
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
