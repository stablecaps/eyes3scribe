import logging
import re
import sys
from collections import defaultdict
from dataclasses import dataclass, field

from rich import print as rprint

from bashautodoc.helpo import hfile, hstrops
from bashautodoc.models.rst2md_converter_anchors import (
    Rst2MdConverter2AnchorsEnd1,
    Rst2MdConverter2AnchorsStart2,
)
from bashautodoc.models.rst2md_converter_triple_colonic_bypass import (
    Rst2mdConverterTripleColonicBypass,
)
from bashautodoc.regex_patterns import *

LOG = logging.getLogger(__name__)


@dataclass()
class Rst2MdDataHolder:
    hwdoc_rpath: str = None
    hwdoc_root: str = None
    hwdoc_name: str = None
    filetext: str = None
    toc_list_clean: list[str] = None
    toclinks_map: dict = None
    md_toc_caption: str = "## Table of Contents"
    md_toclink_list: list[str] = None
    anchorend_detail_map: defaultdict[list] = field(
        default_factory=lambda: defaultdict(list)
    )
    anchorend_fast_map: dict = None
    # anchorend_header_rm_list: list[str] = None


class Rst2MdConverter1Toc:
    def __new__(cls, cnf, hwdoc_rpath) -> None:
        cls.project_docs_dir = cnf.get("project_docs_dir") + "/"
        cls.hwdoc_rpath = hwdoc_rpath
        LOG.debug("hwdoc_rpath: %s", cls.hwdoc_rpath)

        ### init data structures
        cls.r2m = Rst2MdDataHolder()
        cls.r2m.toc_list_clean = []
        cls.r2m.toclinks_map = {}
        cls.r2m.md_toclink_list = []

        cls.r2m.hwdoc_rpath = hwdoc_rpath
        cls.r2m.hwdoc_root, cls.r2m.hwdoc_name = hwdoc_rpath.rsplit("/", 1)
        LOG.debug("\nhwdoc_rpath: %s", hwdoc_rpath)
        LOG.debug(
            "\nhwdoc_root, hwdoc_name = %s, %s", cls.r2m.hwdoc_root, cls.r2m.hwdoc_name
        )

        return cls.main()

    @classmethod
    def gen_markdown_toclinks(cls):
        """
        Generates the markdown table of contents link list.

        Args:
            toc_list_clean (list): The clean table of contents list.
            hwdoc_root (str): The root of the document.

        Returns:
            list: The markdown table of contents link list.
        """
        # TODO: make this function less horrific
        rprint("hwdoc_root", cls.r2m.hwdoc_root)
        # toclinks_map = {}
        # md_toclink_list = []
        for toc_link_name in cls.r2m.toc_list_clean:
            rprint("toc_link_name", toc_link_name)

            if ":caption:" in toc_link_name:
                # TODO: add caption to the toclinks as a h2 header
                cls.r2m.toclinks_map["caption"] = toc_link_name.replace(
                    ":caption:", ""
                ).strip()

            elif ":glob: true" in toc_link_name:
                rprint("\nsearching for globs")
                file_path_list = sorted(
                    hfile.list_matching_files_recursively(
                        search_path=cls.r2m.hwdoc_root,
                        myglob=f"*.md",
                    )
                )
                rprint("file_link_list0", file_path_list)
                for file_path in file_path_list:
                    file_root, file_name = file_path.rsplit("/", 1)
                    # rprint("file_root, file_name = ", file_root, file_name)
                    md_rel_link_clean = file_path.replace(cls.project_docs_dir, "")
                    md_rel_link = f"- [**{file_name.capitalize().replace('/index', '').replace('.md', '')}**]({md_rel_link_clean})"
                    cls.r2m.md_toclink_list.append(md_rel_link)

                    ###
                    cls.r2m.toclinks_map[
                        file_name.replace(".md", "")
                    ] = file_path.replace(cls.project_docs_dir, "")

                rprint("toclinks_map", cls.r2m.toclinks_map)
                rprint("md_toclink_list", cls.r2m.md_toclink_list)
                # sys.exit(42)
                return
            else:
                rprint("\nsearching for", f"{toc_link_name}.md")
                rprint("search_path", cls.r2m.hwdoc_root)
                file_path_list = hfile.list_matching_files_recursively(
                    search_path=cls.r2m.hwdoc_root,
                    myglob=f"{toc_link_name}.md",
                )
                rprint("file_link_list1", file_path_list)

                if len(file_path_list) > 1:
                    print("ERROR: more than one file found")
                    sys.exit(42)

                # md_rel_link_clean = file_path_list[0]
                md_rel_link_clean = file_path_list[0].replace(cls.project_docs_dir, "")
                print("md_rel_link_clean", md_rel_link_clean)
                # sys.exit(42)
                md_rel_link = f"- [**{toc_link_name.capitalize().replace('/index', '')}**]({md_rel_link_clean})"
                # rprint(type(cls.r2m.md_toclink_list))
                cls.r2m.md_toclink_list.append(md_rel_link)

                ###
                cls.r2m.toclinks_map[
                    toc_link_name.replace("/index", "")
                ] = md_rel_link_clean
        return

    @classmethod
    def main(cls):
        rprint("\n\n########################################################")
        rprint("########################################################")
        rprint("\nhwdoc_rpath", cls.hwdoc_rpath)
        rprint("\nhwdoc_root, hwdoc_name =", cls.r2m.hwdoc_root, cls.r2m.hwdoc_name)

        # 1. establish if rst file has a TOC
        cls.r2m.filetext = hfile.read_file_2string(filepath=cls.hwdoc_rpath)
        toc_list = hstrops.get_lines_between_tags(filetext=cls.r2m.filetext)
        if len(toc_list) > 0:
            cls.r2m.toc_list_clean = hstrops.clean_list_via_rm_patts(
                input_list=toc_list,
                rm_patt=["maxdepth:", "```"],
                rm_empty_lines=True,
            )
            rprint("toc_list_clean", cls.r2m.toc_list_clean)

            cls.gen_markdown_toclinks()
            # cls.gen_markdown_toclinks(
            #     toc_list_clean=cls.r2m.toc_list_clean, hwdoc_root=cls.r2m.hwdoc_root
            # )
            rprint("md_toclink_list", cls.r2m.md_toclink_list)

            joined_original_toclinks = "\n".join(toc_list)
            joined_md_toclinks = "\n".join(cls.r2m.md_toclink_list)
            joined_md_toclinks_with_headers = (
                cls.r2m.md_toc_caption + "\n" + joined_md_toclinks
            )
            rprint("\njoined_original_toclinks\n", joined_original_toclinks)
            rprint("\njoined_md_toclinks\n", joined_md_toclinks)
            rprint(
                "\njoined_md_toclinks_with_headers\n", joined_md_toclinks_with_headers
            )
            print("\n\n")

            mdtext_replacedtoc = cls.r2m.filetext.replace(
                joined_original_toclinks, joined_md_toclinks_with_headers
            )
            rprint("mdtext_replacedtoc", mdtext_replacedtoc)

            cls.r2m.filetext = mdtext_replacedtoc
        else:
            cls.r2m.toc_list_clean = None
            toclinks_map = None
            cls.r2m.md_toclink_list = None

        #######################################################
        ### Find all the anchor links for {ref} and build ref dict
        # cls.process_anchorend_links()

        rprint("cls.r2m ", cls.r2m)
        return cls.r2m


toclinks_map_all = {}
r2m_list = []

anchorend_detail_map_all = {}
anchorend_fast_map_all = {}


def rst2md_mainroutine(cnf, hwdocs_search_path):
    hwdoc_rpaths = hfile.multiglob_dir_search(
        search_path=hwdocs_search_path,
        glob_patt_list=["*.md"],
    )

    ### For every rst file
    # 1. establish if it has a TOC
    # 2. convert rst toc lkinks to makrkdown links
    # 3. return a  Rst2MdDataHolder object with relevant data
    # 4. store the Rst2MdDataHolder object in a list
    # 5. convert {ref} links to markdown links

    for hwdoc_rpath in hwdoc_rpaths:
        r2m = Rst2MdConverter1Toc(
            cnf=cnf,
            hwdoc_rpath=hwdoc_rpath,
        )

        toclinks_map_all.update(r2m.toclinks_map)

        r2m_v2 = Rst2MdConverter2AnchorsEnd1(r2m=r2m)

        anchorend_detail_map_all.update(r2m_v2.anchorend_detail_map)

        anchorend_fast_map_all.update(r2m_v2.anchorend_fast_map)
        r2m_list.append(r2m_v2)

        # if "proxy_support" in hwdoc_rpath:
        #     sys.exit(42)

    rprint("\ntoclinks_map_all:")
    for toclink_key, toclink_val in toclinks_map_all.items():
        print("   >>", toclink_key + ":\t", toclink_val)

    rprint("\nanchorend_detail_map_all:")
    for anchor_key, anchor_val in anchorend_detail_map_all.items():
        print("   >>", anchor_key + ":\t", anchor_val)

    rprint("\nanchorend_fast_map_all:")
    for qanchor_key, qanchor_val in anchorend_fast_map_all.items():
        print("   >>", qanchor_key + ":\t", qanchor_val)

    # sys.exit(42)
    ### Replace rst ref links with markdown links
    for r2m in r2m_list:
        rprint("r2m", r2m)
        r2m_v3 = Rst2MdConverter2AnchorsStart2(
            r2m=r2m,
            anchorend_detail_map_all=anchorend_detail_map_all,
            anchorend_fast_map_all=anchorend_fast_map_all,
        )
        rprint("r2m_v3", r2m_v3)
        r2m_v4 = Rst2mdConverterTripleColonicBypass(r2m=r2m_v3)

        # if "themes-list/index" in r2m.hwdoc_rpath:
        #     rprint("r2m.filetext", r2m.filetext)
        #     sys.exit(42)
        hfile.write_string_2file(f"{r2m.hwdoc_root}/{r2m.hwdoc_name}", r2m_v4.filetext)
    # sys.exit(42)
