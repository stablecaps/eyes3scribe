import copy
import logging
import re
import sys
from collections import defaultdict
from dataclasses import dataclass, field

from rich import print as rprint

from eyes3scribe.helpo import hcollections, hfile, hstrops

LOG = logging.getLogger(__name__)


@dataclass()
class Rst2MdDataHolder:
    hwdoc_rpath: str = None
    hwdoc_root: str = None
    hwdoc_name: str = None
    index_name: str = None
    filetext: str = None
    toc_list_clean: list[str] = None
    toclinks_map: defaultdict[list] = field(default_factory=lambda: defaultdict(list))
    md_toc_caption: str = "## Table of Contents"
    mdtoclink_list: list[str] = None
    anchorend_detail_map: defaultdict[list] = field(
        default_factory=lambda: defaultdict(list)
    )
    anchorend_fast_map: dict = None
    # anchorend_header_rm_list: list[str] = None


class Rst2MdConverter1Toc:
    def __new__(cls, cnf, hwdoc_rpath) -> None:
        cls.project_docs_dir = cnf.get("project_docs_dir") + "/"
        cls.handwritten_docs_outdir = cnf.get("handwritten_docs_outdir") + "/"
        cls.hwdoc_rpath = hwdoc_rpath
        LOG.debug("hwdoc_rpath: %s", cls.hwdoc_rpath)

        ### init data structures
        cls.r2m = Rst2MdDataHolder()
        cls.r2m.toc_list_clean = []
        cls.r2m.toclinks_map = defaultdict(list)
        cls.r2m.mdtoclink_list = []

        cls.r2m.hwdoc_rpath = hwdoc_rpath
        cls.r2m.hwdoc_root, cls.r2m.hwdoc_name = hwdoc_rpath.rsplit("/", 1)
        LOG.debug("\nhwdoc_rpath: %s", hwdoc_rpath)
        LOG.debug(
            "\nhwdoc_root, hwdoc_name = %s, %s", cls.r2m.hwdoc_root, cls.r2m.hwdoc_name
        )

        return cls.run()

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
        for toc_link_name in cls.r2m.toc_list_clean:
            rprint("toc_link_name", toc_link_name)

            if ":caption:" in toc_link_name:
                cls.r2m.toclinks_map["caption"] = hstrops.replace_str_pline(
                    toc_link_name, [(":caption:", "")]
                )

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
                    ### version 1
                    # _, file_name = file_path.rsplit("/", 1)
                    # ### As index is in same directory as the file, we need to just use the filename as
                    # ### the relative link. However as we are updating dict, we need another variable
                    # ### for filepath_clean replacemnet within the md file toclink itself
                    # ### probably have to do it downstream as it ddoes not work here

                    # filepath_clean = file_path.replace(cls.handwritten_docs_outdir, "")
                    # mdlink_rel = f"- [**{file_name.capitalize().replace('/index', '').replace('.md', '')}**]({filepath_clean})"
                    # cls.r2m.mdtoclink_list.append(mdlink_rel)
                    # print("cls.handwritten_docs_outdir", cls.handwritten_docs_outdir)
                    # print("file_path", file_path)
                    # print("filepath_clean", filepath_clean)
                    # print("mdlink_rel", mdlink_rel)
                    # # sys.exit(42)

                    # ###
                    # cls.r2m.toclinks_map[
                    #     file_name.replace(".md", "")
                    # ] = file_path.replace(cls.project_docs_dir, "")

                    ### version 2
                    toclink_filepath_clean = copy.deepcopy(file_path).replace(
                        cls.project_docs_dir, ""
                    )
                    print("toclink_filepath_clean", toclink_filepath_clean)
                    filename = file_path.split("/")[-1]
                    mdlink_rel = f"- [**{toc_link_name.capitalize().replace('/index', '')}**]({filename})"
                    cls.r2m.mdtoclink_list.append(mdlink_rel)
                    cls.r2m.toclinks_map[cls.r2m.index_name].append(
                        toclink_filepath_clean
                    )

                rprint("toclinks_map", cls.r2m.toclinks_map)
                rprint("mdtoclink_list", cls.r2m.mdtoclink_list)
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

                ### Version 1
                # filepath_clean = file_path_list[0].replace(cls.project_docs_dir, "")
                # print("filepath_clean", filepath_clean)
                # # sys.exit(42)
                # toc_link_name_noidx = toc_link_name.replace("/index", "")
                # mdlink_rel = (
                #     f"- [**{toc_link_name_noidx.capitalize()}**]({filepath_clean})"
                # )
                # # rprint(type(cls.r2m.mdtoclink_list))
                # cls.r2m.mdtoclink_list.append(mdlink_rel)

                # ###
                # cls.r2m.toclinks_map[toc_link_name_noidx] = filepath_clean

                ### Version 2
                toclink_filepath_clean = copy.deepcopy(file_path_list[0]).replace(
                    cls.project_docs_dir, ""
                )
                print("toclink_filepath_clean", toclink_filepath_clean)
                filename = file_path_list[0].split("/")[-1]
                mdlink_rel = f"- [**{toc_link_name.capitalize().replace('/index', '')}**]({filename})"
                cls.r2m.mdtoclink_list.append(mdlink_rel)
                cls.r2m.toclinks_map[cls.r2m.index_name].append(toclink_filepath_clean)

        return

    @classmethod
    def run(cls):
        rprint("\n\n########################################################")
        rprint("########################################################")
        rprint("\nhwdoc_rpath", cls.hwdoc_rpath)
        rprint("\nhwdoc_root, hwdoc_name =", cls.r2m.hwdoc_root, cls.r2m.hwdoc_name)

        # 1. establish if rst file has a TOC
        cls.r2m.filetext = hfile.read_file_2string(filepath=cls.hwdoc_rpath)
        toc_list = hstrops.get_lines_between_tags(
            filetext=cls.r2m.filetext, start_tag="```{toctree}", end_tag="```"
        )
        if len(toc_list) > 0:
            cls.r2m.index_name = cls.r2m.hwdoc_rpath.replace(cls.project_docs_dir, "")
            print("index_name", cls.r2m.index_name)

            cls.r2m.toc_list_clean = hcollections.clean_list_via_rm_patts(
                input_list=toc_list,
                rm_patts=["maxdepth:", "```"],
                rm_empty_instrs=True,
            )
            rprint("toc_list_clean", cls.r2m.toc_list_clean)

            cls.gen_markdown_toclinks()
            rprint("mdtoclink_list", cls.r2m.mdtoclink_list)

            joined_original_toclinks = "\n".join(toc_list)
            joined_md_toclinks = "\n".join(cls.r2m.mdtoclink_list)
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
                joined_original_toclinks,
                joined_md_toclinks_with_headers,
            )
            rprint("mdtext_replacedtoc", mdtext_replacedtoc)
            # sys.exit(42)

            cls.r2m.filetext = mdtext_replacedtoc

        rprint("cls.r2m ", cls.r2m)
        return cls.r2m
