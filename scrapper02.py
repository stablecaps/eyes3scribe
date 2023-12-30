import logging
import re
import sys
from collections import defaultdict
from dataclasses import dataclass

from rich import print as rprint

from bashautodoc.helpo import hfile, hstrops

# from bashautodoc.helpo.hstrops import search_list_4pattern
from bashautodoc.helpo.hsubprocess import run_cmd_with_output
from bashautodoc.models.filepath_datahandler import FilepathDatahandler

LOG = logging.getLogger(__name__)


@dataclass()
class Rst2MdDataHolder:
    """
    Dataclass to hold data for a file.
    """

    hwdoc_root: str = None
    hwdoc_name: str = None
    filetext: str = None
    toc_list_cleaned: list[str] = None
    toclinks_dict: dict = None
    md_toc_caption: str = "## Table of Contents"
    md_toclink_list: list[str] = None


class Rst2MdTocConverter1:
    def __new__(cls, hwdoc_rpath) -> None:
        cls.hwdoc_rpath = hwdoc_rpath
        LOG.debug("hwdoc_rpath: %s", cls.hwdoc_rpath)

        ### init data structures
        cls.r2m = Rst2MdDataHolder()
        cls.r2m.toc_list_cleaned = []
        cls.r2m.toclinks_dict = {}
        cls.r2m.md_toclink_list = []

        cls.r2m.hwdoc_root, cls.r2m.hwdoc_name = hwdoc_rpath.rsplit("/", 1)
        LOG.debug("\nhwdoc_rpath", hwdoc_rpath)
        LOG.debug("\nhwdoc_root, hwdoc_name =", cls.r2m.hwdoc_root, cls.r2m.hwdoc_name)
        ###
        # cls.toclinks_dict_all = {}
        # cls.mdtext_replacedtoc_data1_list_all = []
        # cls.mdtext_replacedtoc_data2_tuples_all = []

        return cls.main()

    # TODO: Move to hstrops as a generalised function
    @staticmethod
    def clean_rst_toc_list(toc_list):
        """
        Cleans the table of contents RST list.

        Args:
            toc_list (list): The table of contents list in RST format.

        Returns:
            list: The cleaned table of contents list.
        """
        cleaned_toc_list = [
            line
            for line in toc_list
            if (len(line) != 0) and ("maxdepth:" not in line) and ("```" not in line)
        ]
        return cleaned_toc_list

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
                # TODO: add caption to the toclinks as a h3 header
                cls.r2m.md_toc_caption += (
                    "\n### " + toc_link_name.replace(":caption:", "").strip()
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
                    file_root, file_name = file_path.rsplit("/", 1)
                    # rprint("file_root, file_name = ", file_root, file_name)
                    md_rel_link_cleaned = file_path
                    md_rel_link = f"- [**{file_name.capitalize().replace('/index', '').replace('.md', '')}**]({md_rel_link_cleaned})"
                    cls.r2m.md_toclink_list.append(md_rel_link)

                    ###
                    cls.r2m.toclinks_dict[file_name.replace(".md", "")] = file_path

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

                md_rel_link_cleaned = file_path_list[0]
                md_rel_link = f"- [**{toc_link_name.capitalize().replace('/index', '')}**]({md_rel_link_cleaned})"
                # rprint(type(cls.r2m.md_toclink_list))
                cls.r2m.md_toclink_list.append(md_rel_link)

                ###
                cls.r2m.toclinks_dict[
                    toc_link_name.replace("/index", "")
                ] = md_rel_link_cleaned
        return

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
            cls.r2m.toc_list_cleaned = Rst2MdTocConverter1.clean_rst_toc_list(toc_list)
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
            cls.r2m.filetext = mdtext_replacedtoc
        else:
            cls.r2m.toc_list_cleaned = None
            toclinks_dict = None
            cls.r2m.md_toclink_list = None

        rprint("cls.r2m ", cls.r2m)
        return cls.r2m


def generate_ref_sub_tuplist(mdtext, ref_patt, toclinks_dict):
    """
    Generates a list of tuples for ref sub.

    Args:
        mdtext (str): The text with replaced table of contents links.
        ref_patt (re.Pattern): The compiled regular expression pattern for refs.
        toclinks_dict (dict): The dictionary of table of contents links.

    Returns:
        list: The list of tuples for ref sub.
    """

    ref_sub_tuplist = []
    for line in mdtext.split("\n"):
        if "{ref}" in line:
            ref_match = re.search(ref_patt, line)
            if ref_match is not None:
                # ref_anchor = ref_match.group(1).strip()
                ref_title = ref_match.group(2).replace("`", "").strip()
                toc_link_key = (
                    ref_match.group(3)
                    .replace("`", "")
                    .replace("<", "")
                    .replace(">", "")
                    .strip()
                )
                rst_ref_string = (
                    f"{ref_match.group(1)}{ref_match.group(2)}{ref_match.group(3)}"
                )

                if toclinks_dict.get(toc_link_key) is None:
                    print(f"ERROR: toc_link_key not found: {toc_link_key}")
                    print("toclinks_dict keys", toclinks_dict.keys())
                    # sys.exit(42)
                else:
                    toc_link_value = toclinks_dict[toc_link_key]
                    md_ref_link = f"[{ref_title}]({toc_link_value})"
                    ref_sub_tuplist.append((rst_ref_string, md_ref_link))

    return ref_sub_tuplist


def replace_refs_with_links(mdtext, ref_sub_tuplist):
    """
    Replaces refs with links in the text with replaced table of contents links.

    Args:
        mdtext (str): The text with replaced table of contents links.
        ref_sub_tuplist (list): The list of tuples for ref sub.

    Returns:
        str: The text with refs replaced with links.
    """
    mdtext_replaced = mdtext
    for rst_ref_string, md_ref_link in ref_sub_tuplist:
        mdtext_replaced = mdtext_replaced.replace(rst_ref_string, md_ref_link)

    return mdtext_replaced


toclinks_dict_all = {}
r2m_list = []

ref_patt = re.compile(r"({ref})(`[a-zA-Z0-9-. ]*)(<[a-zA-Z`]*>`)")
leftover_path = re.compile(r"^\([a-z.A-Z0-9]*\)=$")

if __name__ == "__main__":
    hwdoc_rpaths = hfile.multiglob_dir_search(
        search_path="./docs_bash-it/docs/docshw/",
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
            hwdoc_rpath=hwdoc_rpath,
        )

        # if len(r2m.toclinks_dict) > 0:
        #     rprint("sorted dict test")
        #     sys.exit(42)

        toclinks_dict_all.update(r2m.toclinks_dict)
        r2m_list.append(r2m)

    for toclink_key, toclink_val in toclinks_dict_all.items():
        print("   >>", toclink_key + ":\t", toclink_val)

    rprint("jabba", toclinks_dict_all)
    # sys.exit(42)

    for r2m in r2m_list:
        rprint("r2m", r2m)
        ref_sub_tuplist = generate_ref_sub_tuplist(
            mdtext=r2m.filetext,
            ref_patt=ref_patt,
            toclinks_dict=toclinks_dict_all,
        )
        mdtext_replacedrefs = replace_refs_with_links(
            mdtext=r2m.filetext, ref_sub_tuplist=ref_sub_tuplist
        )
        r2m.filetext = mdtext_replacedrefs

        # sys.exit(42)
        hfile.write_string_2file(f"{r2m.hwdoc_root}/{r2m.hwdoc_name}", r2m.filetext)
