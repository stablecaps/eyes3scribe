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


def gen_img_html(rst_img_dict):
    """
    rst_img_dict = {
        "image": None,
        "height": None,
        "width": None,
        "scale": None,
        "loading": None,
        "alt": None,
        "align": None,

    <a class="reference external image-reference" href="https://raw.githubusercontent.com/lfelipe1501/lfelipe-projects/master/AtomicTheme.gif"><img alt="Atomic-Theme" src="https://raw.githubusercontent.com/lfelipe1501/lfelipe-projects/master/AtomicTheme.gif"></a>
    }
    """
    img_html = textwrap.dedent(
        f"""<a class="reference external image-reference"
                href="{rst_img_dict.get('image')}"><img alt="{rst_img_dict.get('alt')}" src="{rst_img_dict.get('image')}">
                </a>
         """
    )
    return img_html


class Rst2mdConverterTripleColonicBypass:
    def __new__(
        cls,
        r2m,
    ):
        cls.r2m = r2m

        return cls.main()

    @classmethod
    def process_mdlink_in_admon(cls, mdlink_in_admon, admon_text):
        mdlink_in_admon_str = mdlink_in_admon.group(0)
        # rprint("mdlink_in_admon", mdlink_in_admon)

        # <a href="./document.html">Document</a>
        html_link = (
            f'<a href="{mdlink_in_admon.group(2)}">{mdlink_in_admon.group(1)}</a>'
        )
        admon_text = admon_text.replace(
            mdlink_in_admon_str,
            html_link,
        )
        # rprint("admon_text", admon_text)
        # rprint(
        #     "mdlink_in_admon_str",
        #     mdlink_in_admon_str,
        # )
        # rprint("html_link", html_link)
        return admon_text

    @classmethod
    def process_admon_match(cls, admon_match, block):
        admon_type = admon_match.group(1)
        admon_text = "\n".join(block[1:-1])
        # rprint(
        #     "admon_type, admon_text = ",
        #     admon_type,
        #     admon_text,
        # )

        mdlink_in_admon = re.search(mdlink_patt, admon_text)
        if mdlink_in_admon:
            admon_text = cls.process_mdlink_in_admon(mdlink_in_admon, admon_text)

        admon_html_notitle = gen_admon_html_notitle(
            admon_type=admon_type, admod_text=admon_text
        )

        admon_rst_text = "\n".join(block)

        # rprint("admon_html_notitle", admon_html_notitle)
        # rprint("admon_rst_text", admon_rst_text)

        cls.r2m.filetext = cls.r2m.filetext.replace(
            admon_rst_text,
            admon_html_notitle,
        )
        # rprint("\ncls.r2m.filetext", cls.r2m.filetext)

    @classmethod
    def process_admon_block(cls, block):
        # rprint("admon_block:", block)

        # rprint("\nblock: ", block)
        # rprint("xxxx", admon_patt_multiline_start, block[0])
        admon_match = re.search(admon_patt_multiline_start, block[0])
        # rprint("admon_match: ", admon_match)
        if admon_match:
            cls.process_admon_match(admon_match, block)

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
                    cls.process_admon_block(block)

    @classmethod
    def process_image_element(cls, elem, rst_img_dict):
        # rprint("elem", elem)
        if elem.startswith("```{image}"):
            rst_img_dict["image"] = hstrops.clean_str_via_rm_patts(
                input_str=elem, rm_patterns=["```{image}"]
            )

        elif elem.startswith(":alt:"):
            rst_img_dict["alt"] = hstrops.clean_str_via_rm_patts(
                input_str=elem, rm_patterns=[":alt:"]
            )
        elif elem.startswith(":height:"):
            rst_img_dict["height"] = hstrops.clean_str_via_rm_patts(
                input_str=elem, rm_patterns=[":height:"]
            )
        elif elem.startswith(":width:"):
            rst_img_dict["width"] = hstrops.clean_str_via_rm_patts(
                input_str=elem, rm_patterns=[":width:"]
            )
        elif elem.startswith(":width:"):
            rst_img_dict["scale"] = hstrops.clean_str_via_rm_patts(
                input_str=elem, rm_patterns=[":width:"]
            )
        elif elem.startswith(":loading:"):
            rst_img_dict["loading"] = hstrops.clean_str_via_rm_patts(
                input_str=elem, rm_patterns=[":loading:"]
            )
        elif elem.startswith(":loading:"):
            rst_img_dict["align"] = hstrops.clean_str_via_rm_patts(
                input_str=elem, rm_patterns=[":loading:"]
            )

    @classmethod
    def process_image_block(cls, block):
        # rprint("block", block)
        rst_img_dict = {
            "image": None,
            "height": None,
            "width": None,
            "scale": None,
            "loading": None,
            "alt": None,
            "align": None,
        }
        for elem in block:
            cls.process_image_element(elem, rst_img_dict)

        # rprint("rst_img_dict", rst_img_dict)

        img_html = gen_img_html(rst_img_dict=rst_img_dict)
        # rprint("img_html", img_html)

        img_rst = "\n".join(block)
        # rprint("img_html", img_html)
        # rprint("img_rst", img_rst)

        cls.r2m.filetext = cls.r2m.filetext.replace(
            img_rst,
            img_html,
        )
        # rprint("\ncls.r2m.filetext", cls.r2m.filetext)
        # sys.exit(42)

    @classmethod
    def process_hosted_images(cls):
        """
        https://docutils.sourceforge.io/docs/ref/rst/directives.html#image
        """
        if "```{image}" in cls.r2m.filetext:
            himage_blocks_nlist = (
                hstrops.extract_multiblocks_between_start_and_end_line_tag(
                    filetext=cls.r2m.filetext, start_tag="```{image}", end_tag="```"
                )
            )
            rprint("himage_blocks_nlist", himage_blocks_nlist)
            # sys.exit(42)
            if len(himage_blocks_nlist) > 0:
                for block in himage_blocks_nlist:
                    cls.process_image_block(block)

    @classmethod
    def main(cls):
        cls.process_admonitions()

        cls.process_hosted_images()

        return cls.r2m
