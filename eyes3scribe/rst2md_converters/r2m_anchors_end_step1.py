import copy
import logging
import re

from rich import print as rprint

from eyes3scribe.helpo import hstrops
from eyes3scribe.regex_patterns import anchorend_patt, hxhash_patt

LOG = logging.getLogger(__name__)


class R2MAnchorsEndStep1:
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
                        instr=(anchorend_key.replace("(", "").replace(")=", "").strip())
                    )

                    hxhash_match = re.search(hxhash_patt, anchorend_header_line)
                    if hxhash_match:
                        # '#  <a id="contributing></a> Contribution Guidelines'
                        anchorend_link = R2MAnchorsEndStep1.gen_anchorend_link(
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
