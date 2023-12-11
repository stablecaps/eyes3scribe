import logging
import re
import sys
from collections import defaultdict

from rich import print as rprint

import bashautodoc.helpo.hfile as hfile

# from bashautodoc.helpo.hstrops import search_list_4pattern
from bashautodoc.helpo.hsubprocess import run_cmd_with_output
from bashautodoc.models.filepath_datahandler import FilepathDatahandler

toclinks_dict = {}


def extract_lines_between_tags(filetext):
    """
    Extracts lines between tags in the file text.

    Args:
        file_text (str): The text of the file.

    Returns:
        list: The lines between tags in the file text.
    """
    line_holder = []
    inRecordingMode = False
    for line in filetext.split("\n"):
        # line_stripped = line.strip()
        if not inRecordingMode:
            if "```{toctree}" in line:
                rprint("TRUE: found toctree")
                inRecordingMode = True
                line_holder.append(line)
        elif "```" in line:
            inRecordingMode = False
            line_holder.append(line)
        else:
            line_holder.append(line)

    return line_holder


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
        if (line != "") and ("maxdepth:" not in line) and ("```" not in line)
    ]
    return cleaned_toc_list


def generate_md_toclink_data(toc_list_cleaned, toc_root):
    """
    Generates the markdown table of contents link list.

    Args:
        toc_list_cleaned (list): The cleaned table of contents list.
        toc_root (str): The root of the document.

    Returns:
        list: The markdown table of contents link list.
    """
    toclinks_dict = {}
    md_toclink_list = []
    for toc_link_name in toc_list_cleaned:
        file_link_list = hfile.list_matching_files_recursively(
            search_path=toc_root,
            myglob=f"{toc_link_name}.md",
        )

        if len(file_link_list) > 1:
            print("ERROR: more than one file found")
            sys.exit(42)

        md_rel_link_cleaned = file_link_list[0]
        md_rel_link = f"- [**{toc_link_name.capitalize().replace('/index', '')}**]({md_rel_link_cleaned})"
        md_toclink_list.append(md_rel_link)

        ###
        toclinks_dict[toc_link_name.replace("/index", "")] = md_rel_link_cleaned

    return (toclinks_dict, md_toclink_list)


def convert_rst_2md_toclinks(search_path, glob_pattern_list):
    hwdoc_relpaths = hfile.search_directory_with_multiple_globs(
        search_path=search_path,
        glob_patt_list=glob_pattern_list,
    )
    rprint("hwdoc_relpaths: %s", hwdoc_relpaths)

    for hwdoc_relpath in hwdoc_relpaths:
        hwdoc_root, hwdoc_extension = hwdoc_relpath.rsplit("/", 1)
        rprint("\nhwdoc_relpath", hwdoc_relpath)
        rprint("\nhwdoc_root", hwdoc_root, hwdoc_extension)
        if "index" in hwdoc_relpath:
            rprint("\nhwdoc_relpath", hwdoc_relpath)
            filetext = hfile.read_file_2string(filepath=hwdoc_relpath)
            # rprint("\nfiletext: %s", filetext)
            rprint("\n\n")

            toc_list = extract_lines_between_tags(filetext=filetext)
            toc_list_cleaned = clean_rst_toc_list(toc_list)
            rprint("\ntoc_list: %s", toc_list)
            print("toc_list_cleaned", toc_list_cleaned)

            toclinks_dict, md_toclink_list = generate_md_toclink_data(
                toc_list_cleaned=toc_list_cleaned, toc_root=hwdoc_root
            )
            print("md_toclink_list", md_toclink_list)

            joined_original_toclinks = "\n".join(toc_list)
            joined_md_toclinks = "\n".join(md_toclink_list)
            rprint("\njoined_original_toclinks\n", joined_original_toclinks)
            rprint("\njoined_md_toclinks\n", joined_md_toclinks)
            print("\n\n")

            mdtext_replacedtoc = filetext.replace(
                joined_original_toclinks, joined_md_toclinks
            )
            print("mdtext_replacedtoc\n", mdtext_replacedtoc)

            return toclinks_dict, mdtext_replacedtoc


###########
def generate_ref_sub_tuplist(mdtext_replacedtoc, ref_patt, toclinks_dict):
    """
    Generates a list of tuples for ref sub.

    Args:
        mdtext_replacedtoc (str): The text with replaced table of contents links.
        ref_patt (re.Pattern): The compiled regular expression pattern for refs.
        toclinks_dict (dict): The dictionary of table of contents links.

    Returns:
        list: The list of tuples for ref sub.
    """

    ref_sub_tuplist = []
    for line in mdtext_replacedtoc.split("\n"):
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
                    print("ERROR: toc_link_key not found")
                    sys.exit(42)
                else:
                    toc_link_value = toclinks_dict[toc_link_key]
                    md_ref_link = f"[{ref_title}]({toc_link_value})"
                    ref_sub_tuplist.append((rst_ref_string, md_ref_link))

    return ref_sub_tuplist


def replace_refs_with_links(mdtext_replacedtoc, ref_sub_tuplist):
    """
    Replaces refs with links in the text with replaced table of contents links.

    Args:
        mdtext_replacedtoc (str): The text with replaced table of contents links.
        ref_sub_tuplist (list): The list of tuples for ref sub.

    Returns:
        str: The text with refs replaced with links.
    """
    mdtext_replacedrefs = mdtext_replacedtoc
    for rst_ref_string, md_ref_link in ref_sub_tuplist:
        mdtext_replacedrefs = mdtext_replacedrefs.replace(rst_ref_string, md_ref_link)

    return mdtext_replacedrefs


if __name__ == "__main__":
    ref_patt = re.compile(r"({ref})(`[a-zA-Z0-9-. ]*)(<[a-zA-Z`]*>`)")
    toclinks_dict, mdtext_replacedtoc = convert_rst_2md_toclinks(
        search_path="./docs_bash-it/docs/docshw/", glob_pattern_list=["*.md"]
    )

    print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")

    ref_sub_tuplist = generate_ref_sub_tuplist(
        mdtext_replacedtoc=mdtext_replacedtoc,
        ref_patt=ref_patt,
        toclinks_dict=toclinks_dict,
    )

    for toclink_key, toclink_val in toclinks_dict.items():
        print("   >>", toclink_key + ":\t", toclink_val)

    print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
    mdtext_replacedrefs = replace_refs_with_links(
        mdtext_replacedtoc=mdtext_replacedtoc, ref_sub_tuplist=ref_sub_tuplist
    )

    print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
    print("mdtext_replacedrefs\n", mdtext_replacedrefs)
