import logging
import re
import sys
from collections import defaultdict
from dataclasses import dataclass, field

from rich import print as rprint

from bashautodoc.helpo import hfile, hstrops
from bashautodoc.models.ref_anchor_converter import RefAnchorConverter
from bashautodoc.regex_patterns import *

LOG = logging.getLogger(__name__)


@dataclass()
class Rst2MdDataHolder:
    """
    Dataclass to hold data for a file.
    """

    hwdoc_rpath: str = None
    hwdoc_root: str = None
    hwdoc_name: str = None
    filetext: str = None
    toc_list_cleaned: list[str] = None
    toclinks_dict: dict = None
    md_toc_caption: str = "## Table of Contents"
    md_toclink_list: list[str] = None
    anchorlinks_verbose_dict: defaultdict[list] = field(
        default_factory=lambda: defaultdict(list)
    )
    anchorlinks_quickmap_dict: dict = None
    end_anchors_2hx_replace_list: list[str] = None


class Rst2MdTocConverter1:
    def __new__(cls, conf, hwdoc_rpath) -> None:
        cls.project_docs_dir = conf.get("project_docs_dir") + "/"
        cls.hwdoc_rpath = hwdoc_rpath
        LOG.debug("hwdoc_rpath: %s", cls.hwdoc_rpath)

        ### init data structures
        cls.r2m = Rst2MdDataHolder()
        cls.r2m.toc_list_cleaned = []
        cls.r2m.toclinks_dict = {}
        cls.r2m.md_toclink_list = []
        #
        # cls.r2m.anchorlinks_verbose_dict = {}
        cls.r2m.anchorlinks_quickmap_dict = {}

        cls.r2m.hwdoc_rpath = hwdoc_rpath
        cls.r2m.hwdoc_root, cls.r2m.hwdoc_name = hwdoc_rpath.rsplit("/", 1)
        LOG.debug("\nhwdoc_rpath: %s", hwdoc_rpath)
        LOG.debug(
            "\nhwdoc_root, hwdoc_name = %s, %s", cls.r2m.hwdoc_root, cls.r2m.hwdoc_name
        )
        ###
        # cls.toclinks_dict_all = {}
        # cls.mdtext_replacedtoc_data1_list_all = []
        # cls.mdtext_replacedtoc_data2_tuples_all = []

        return cls.main()

    @classmethod
    def create_markdown_toclinks(cls):
        """
        Generates the markdown table of contents link list.

        Args:
            toc_list_cleaned (list): The cleaned table of contents list.
            hwdoc_root (str): The root of the document.

        Returns:
            list: The markdown table of contents link list.
        """
        # TODO: make this function less horrific
        rprint("hwdoc_root", cls.r2m.hwdoc_root)
        # toclinks_dict = {}
        # md_toclink_list = []
        for toc_link_name in cls.r2m.toc_list_cleaned:
            rprint("toc_link_name", toc_link_name)

            if ":caption:" in toc_link_name:
                # TODO: add caption to the toclinks as a h2 header
                cls.r2m.toclinks_dict["caption"] = toc_link_name.replace(
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
                    md_rel_link_cleaned = file_path.replace(cls.project_docs_dir, "")
                    md_rel_link = f"- [**{file_name.capitalize().replace('/index', '').replace('.md', '')}**]({md_rel_link_cleaned})"
                    cls.r2m.md_toclink_list.append(md_rel_link)

                    ###
                    cls.r2m.toclinks_dict[
                        file_name.replace(".md", "")
                    ] = file_path.replace(cls.project_docs_dir, "")

                rprint("toclinks_dict", cls.r2m.toclinks_dict)
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

                # md_rel_link_cleaned = file_path_list[0]
                md_rel_link_cleaned = file_path_list[0].replace(
                    cls.project_docs_dir, ""
                )
                print("md_rel_link_cleaned", md_rel_link_cleaned)
                # sys.exit(42)
                md_rel_link = f"- [**{toc_link_name.capitalize().replace('/index', '')}**]({md_rel_link_cleaned})"
                # rprint(type(cls.r2m.md_toclink_list))
                cls.r2m.md_toclink_list.append(md_rel_link)

                ###
                cls.r2m.toclinks_dict[
                    toc_link_name.replace("/index", "")
                ] = md_rel_link_cleaned
        return

    @classmethod
    def process_anchor_links(cls):
        # 1. search md text for ref links in format "(contributing-theme)="
        # 2. Construct dict mapping "(help-screens)=" to filepath.md (the appropriate header is just after. e.g. "# Help Screens")
        #   Use name of hx header as value. filepath.md is the key.
        #   Note you will have to take next hx header name directly at this stage as names don't match. e.g. "(contributing-theme)=" != "## Themes"
        # 3. Delete the "(help-screens)=" from the md text
        # 4. Replace all {ref} links with markdown anchor links. e.g. "### <a id="command-duration"></a> Command duration"
        # 5. Delete existing hx header. i.e. "### Command duration"  (4 & 5 is a .replace job)
        # anchor_end_pattern = re.compile(r"^(\([a-z.A-Z0-9-_]*\)=)$")
        end_anchors_2hx_replace_list = []
        is_next_line_header = False
        anchor_end_match_string = None
        for line in cls.r2m.filetext.split("\n"):
            anchor_end_match = re.search(anchor_end_pattern, line)

            if anchor_end_match is not None:
                matched_end_anchor = line
                end_anchors_2hx_replace_list.append(matched_end_anchor)
                anchor_end_match_string = anchor_end_match.group(1)
                is_next_line_header = True
                rprint("matched_end_anchor", matched_end_anchor)
                rprint("anchor_end_match", anchor_end_match)
                rprint("is_next_line_header", is_next_line_header)
            elif is_next_line_header:
                if (
                    line.startswith("# ")
                    or line.startswith("## ")
                    or line.startswith("### ")
                    or line.startswith("#### ")
                ):
                    header_line = line
                    rprint("header_line", header_line, is_next_line_header)

                    cleaned_anchor_end_match_string = hstrops.normalise_key(
                        mystr=(
                            anchor_end_match_string.replace("(", "").replace(")=", "")
                        )
                    )
                    cls.r2m.anchorlinks_quickmap_dict[
                        cleaned_anchor_end_match_string
                    ] = cls.r2m.hwdoc_rpath
                    #
                    #
                    cls.r2m.anchorlinks_verbose_dict[cls.r2m.hwdoc_rpath].append(
                        [
                            cleaned_anchor_end_match_string,
                            header_line,
                        ]
                    )
                    is_next_line_header = False
                    # sys.exit(42)

        # for end_anchors in end_anchors_2hx_replace_list:
        #     cls.r2m.filetext = cls.r2m.filetext.replace(end_anchors, "")

    @classmethod
    def main(cls):
        rprint("\n\n########################################################")
        rprint("########################################################")
        rprint("\nhwdoc_rpath", cls.hwdoc_rpath)
        rprint("\nhwdoc_root, hwdoc_name =", cls.r2m.hwdoc_root, cls.r2m.hwdoc_name)

        # 1. establish if rst file has a TOC
        cls.r2m.filetext = hfile.read_file_2string(filepath=cls.hwdoc_rpath)
        toc_list = hstrops.extract_lines_between_tags(filetext=cls.r2m.filetext)
        if len(toc_list) > 0:
            cls.r2m.toc_list_cleaned = hstrops.clean_list_via_rm_patterns(
                input_list=toc_list,
                rm_patterns=["maxdepth:", "```"],
                rm_empty_lines=True,
            )
            rprint("toc_list_cleaned", cls.r2m.toc_list_cleaned)

            cls.create_markdown_toclinks()
            # cls.create_markdown_toclinks(
            #     toc_list_cleaned=cls.r2m.toc_list_cleaned, hwdoc_root=cls.r2m.hwdoc_root
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
            cls.r2m.toc_list_cleaned = None
            toclinks_dict = None
            cls.r2m.md_toclink_list = None

        #######################################################
        ### Find all the anchor links for {ref} and build ref dict
        cls.process_anchor_links()

        rprint("cls.r2m ", cls.r2m)
        return cls.r2m


toclinks_dict_all = {}
r2m_list = []

anchorlinks_verbose_dict_all = {}
anchorlinks_quickmap_dict_all = {}


def rst2md_mainroutine(conf, hwdocs_search_path):
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
        r2m = Rst2MdTocConverter1(
            conf=conf,
            hwdoc_rpath=hwdoc_rpath,
        )

        # if "commands/index" in hwdoc_rpath:
        #     sys.exit(42)

        toclinks_dict_all.update(r2m.toclinks_dict)
        r2m_list.append(r2m)

        anchorlinks_verbose_dict_all.update(r2m.anchorlinks_verbose_dict)

        anchorlinks_quickmap_dict_all.update(r2m.anchorlinks_quickmap_dict)

    rprint("\ntoclinks_dict_all:")
    for toclink_key, toclink_val in toclinks_dict_all.items():
        print("   >>", toclink_key + ":\t", toclink_val)

    rprint("\nanchorlinks_verbose_dict_all:")
    for anchor_key, anchor_val in anchorlinks_verbose_dict_all.items():
        print("   >>", anchor_key + ":\t", anchor_val)

    rprint("\nanchorlinks_quickmap_dict_all:")
    for qanchor_key, qanchor_val in anchorlinks_quickmap_dict_all.items():
        print("   >>", qanchor_key + ":\t", qanchor_val)

    print()
    rprint(anchorlinks_quickmap_dict_all)
    # sys.exit(42)

    ### Replace rst ref links with markdown links
    for r2m in r2m_list:
        rprint("r2m", r2m)
        ref_anchor_converter = RefAnchorConverter(
            r2m=r2m,
            anchorlinks_verbose_dict_all=anchorlinks_verbose_dict_all,
            anchorlinks_quickmap_dict_all=anchorlinks_quickmap_dict_all,
        )
        mdtext_replaced = ref_anchor_converter.main()

        # if "barbuk" in r2m.hwdoc_rpath:
        #     rprint("r2m.filetext", r2m.filetext)
        #     sys.exit(42)
        hfile.write_string_2file(f"{r2m.hwdoc_root}/{r2m.hwdoc_name}", mdtext_replaced)
