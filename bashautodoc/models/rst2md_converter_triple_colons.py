import copy
import logging
import re
import sys
import textwrap
from collections import defaultdict
from dataclasses import dataclass, field

from rich import print as rprint

from bashautodoc.helpo import hfile, hstrops
from bashautodoc.regex_patterns import admon_patt_multiline_start, mdlink_patt

LOG = logging.getLogger(__name__)


def gen_admon_html_notitle(admon_type, admod_text):
    admon_html_notitle = textwrap.dedent(
        f"""
    <div class="admonition {admon_type}">
    <p class="admonition-title">{admon_type.capitalize()}</p>
    <p>{admod_text}</p>
    </div>"""
    )
    return admon_html_notitle


class Rst2mdConverterTripleColons:
    def __new__(
        cls,
        r2m,
    ):
        cls.r2m = r2m

        return cls.main()

    @classmethod
    def process_admonitions(cls):
        if ":::" in cls.r2m.filetext:
            admonitions_blocks_nlist = (
                hstrops.extract_multiblocks_between_start_and_end_line_tag(
                    filetext=cls.r2m.filetext, start_tag=":::", end_tag=":::"
                )
            )

            if len(admonitions_blocks_nlist) > 0:
                for block in admonitions_blocks_nlist:
                    rprint("admon_block:", block)

                    rprint("\nblock: ", block)
                    rprint("xxxx", admon_patt_multiline_start, block[0])
                    admon_match = re.search(admon_patt_multiline_start, block[0])
                    rprint("admon_match: ", admon_match)
                    if admon_match:
                        admon_type = admon_match.group(1)
                        admon_text = "\n".join(block[1:-1])
                        rprint(
                            "admon_type, admon_text = ",
                            admon_type,
                            admon_text,
                        )

                        mdlink_in_admon = re.search(mdlink_patt, admon_text)
                        if mdlink_in_admon:
                            mdlink_in_admon_str = mdlink_in_admon.group(0)
                            rprint("mdlink_in_admon", mdlink_in_admon)

                            # <a href="./document.html">Document</a>
                            html_link = f'<a href="{mdlink_in_admon.group(2)}">{mdlink_in_admon.group(1)}</a>'
                            admon_text = admon_text.replace(
                                mdlink_in_admon_str,
                                html_link,
                            )
                            rprint("admon_text", admon_text)
                            rprint(
                                "mdlink_in_admon_str",
                                mdlink_in_admon_str,
                            )
                            rprint("html_link", html_link)
                            # sys.exit(42)

                        admon_html_notitle = gen_admon_html_notitle(
                            admon_type=admon_type, admod_text=admon_text
                        )

                        admon_rst_text = "\n".join(block)

                        rprint("admon_html_notitle", admon_html_notitle)
                        rprint("admon_rst_text", admon_rst_text)

                        cls.r2m.filetext = cls.r2m.filetext.replace(
                            admon_rst_text,
                            admon_html_notitle,
                        )
                        rprint("\ncls.r2m.filetext", cls.r2m.filetext)

    @classmethod
    def main(cls):
        cls.process_admonitions()

        return cls.r2m
