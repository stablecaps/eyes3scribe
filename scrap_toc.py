import logging
import sys
from collections import defaultdict

from rich import print as rprint

import bashautodoc.helpo.hfile as hfile

# from bashautodoc.helpo.hstrops import search_list_4pattern
from bashautodoc.helpo.hsubprocess import run_cmd_with_output
from bashautodoc.models.filepath_datahandler import FilepathDatahandler


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
        if line != "" and "maxdepth:" not in line and "```" not in line
    ]
    return cleaned_toc_list


def generate_md_toclink_list(toc_list_cleaned, toc_root):
    """
    Generates the markdown table of contents link list.

    Args:
        toc_list_cleaned (list): The cleaned table of contents list.
        toc_root (str): The root of the document.

    Returns:
        list: The markdown table of contents link list.
    """
    md_toc_link_list = []
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
        md_toc_link_list.append(md_rel_link)

    return md_toc_link_list


def replace_original_toclinks_with_new_ones(file_text, original_toclinks, md_toclinks):
    """
    Replaces the original table of contents links with the new ones in the file text.

    Args:
        file_text (str): The text of the file.
        original_toclinks (str): The original table of contents links.
        new_toclinks (str): The new table of contents links.

    Returns:
        str: The text of the file with the original table of contents links replaced with the new ones.
    """
    replaced_file_text = file_text.replace(original_toclinks, md_toclinks)
    return replaced_file_text


def convert_rst_2md_toclinks(search_path, glob_pattern_list):
    hwdoc_relpaths = hfile.search_directory_with_multiple_globs(
        search_path=search_path,
        glob_patt_list=glob_pattern_list,
    )

    rprint("hwdoc_relpaths: %s", hwdoc_relpaths)

    for hwdoc_relpath in hwdoc_relpaths:
        rprint("\nhwdoc_relpath", hwdoc_relpath)
        hwdoc_root, hwdoc_extension = hwdoc_relpath.rsplit("/", 1)
        rprint("\nhwdoc_root", hwdoc_root, hwdoc_extension)
        # sys.exit(42)
        if "index" in hwdoc_relpath:
            rprint("\nhwdoc_relpath", hwdoc_relpath)
            filetext = hfile.read_file_2string(filepath=hwdoc_relpath)
            # rprint("\nfiletext: %s", filetext)

            rprint("\n\n")

            toc_list = extract_lines_between_tags(filetext=filetext)
            rprint("\ntoc_list: %s", toc_list)

            toc_list_cleaned = clean_rst_toc_list(toc_list)
            print("toc_list_cleaned", toc_list_cleaned)
            # sys.exit(42)

            md_toclink_list = generate_md_toclink_list(
                toc_list_cleaned=toc_list_cleaned, toc_root=hwdoc_root
            )
            print("md_toclink_list", md_toclink_list)

            joined_original_toclinks = "\n".join(toc_list)
            rprint("\njoined_original_toclinks\n", joined_original_toclinks)

            joined_md_toclinks = "\n".join(md_toclink_list)
            rprint("\njoined_md_toclinks\n", joined_md_toclinks)
            # sys.exit(42)

            print("\n\n")

            replaced_filetext = replace_original_toclinks_with_new_ones(
                file_text=filetext,
                original_toclinks=joined_original_toclinks,
                md_toclinks=joined_md_toclinks,
            )
            print("replaced_filetext\n", replaced_filetext)
            sys.exit(42)


###########
if __name__ == "__main__":
    convert_rst_2md_toclinks(
        search_path="./docs_bash-it/docs/docshw/", glob_pattern_list=["*.md"]
    )
