import re
import sys

from rich import print as rprint

from bashautodoc.helpo import hfile

toclinks_map = {}


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
        list: The clean table of contents list.
    """
    clean_toc_list = [
        line
        for line in toc_list
        if (len(line) != 0) and ("maxdepth:" not in line) and ("```" not in line)
    ]
    return clean_toc_list


def gen_markdown_toclinks(toc_list_clean, toc_root):
    """
    Generates the markdown table of contents link list.

    Args:
        toc_list_clean (list): The clean table of contents list.
        toc_root (str): The root of the document.

    Returns:
        list: The markdown table of contents link list.
    """
    rprint("toc_root", toc_root)
    toclinks_map = {}
    md_toclink_list = []
    for toc_link_name in toc_list_clean:
        rprint("toc_link_name", toc_link_name)

        if ":caption:" in toc_link_name:
            # TODO: add caption to the toclinks as a h2 header
            toclinks_map["caption"] = toc_link_name.replace(":caption:", "").strip()

        elif ":glob: true" in toc_link_name:
            file_path_list = sorted(
                hfile.list_matching_files_recursively(
                    search_path=toc_root,
                    myglob=f"*.md",
                )
            )
            rprint("file_link_list0", file_path_list)
            for file_path in file_path_list:
                file_root, file_name = file_path.rsplit("/", 1)
                md_rel_link_clean = file_path
                md_rel_link = f"- [**{file_name.capitalize().replace('/index', '').replace('.md', '')}**]({md_rel_link_clean})"
                md_toclink_list.append(md_rel_link)

                ###
                toclinks_map[toc_link_name.replace("/index", "")] = md_rel_link_clean

            rprint("toclinks_map", toclinks_map)
            rprint("md_toclink_list", md_toclink_list)
            return (toclinks_map, md_toclink_list)
        else:
            file_path_list = hfile.list_matching_files_recursively(
                search_path=toc_root,
                myglob=f"{toc_link_name}.md",
            )
            rprint("file_link_list1", file_path_list)

            if len(file_path_list) > 1:
                print("ERROR: more than one file found")
                sys.exit(42)

            md_rel_link_clean = file_path_list[0]
            md_rel_link = f"- [**{toc_link_name.capitalize().replace('/index', '')}**]({md_rel_link_clean})"
            md_toclink_list.append(md_rel_link)

            ###
            toclinks_map[toc_link_name.replace("/index", "")] = md_rel_link_clean

            # if f"{toc_link_name}.md" == "themes-list/index.md":
            #     sys.exit(42)

    return (toclinks_map, md_toclink_list)


# def convert_rst_2markdown_toclinks(hwdoc_rpath):
#     hwdoc_root, hwdoc_extension = hwdoc_rpath.rsplit("/", 1)
#     rprint("\nhwdoc_rpath", hwdoc_rpath)
#     rprint("\nhwdoc_root", hwdoc_root, hwdoc_extension)

#     rprint("\nhwdoc_rpath", hwdoc_rpath)
#     filetext = hfile.read_file_2string(filepath=hwdoc_rpath)
#     # rprint("\nfiletext: %s", filetext)
#     rprint("\n\n")

#     toc_list = extract_lines_between_tags(filetext=filetext)
#     toc_list_clean = clean_rst_toc_list(toc_list)
#     rprint("\ntoc_list: %s", toc_list)
#     print("toc_list_clean", toc_list_clean)
#     if len(toc_list) > 0:
#         sys.exit(42)

#     toclinks_map, md_toclink_list = gen_markdown_toclinks(
#         toc_list_clean=toc_list_clean, toc_root=hwdoc_root
#     )
#     print("md_toclink_list", md_toclink_list)

#     joined_original_toclinks = "\n".join(toc_list)
#     joined_md_toclinks = "\n".join(md_toclink_list)
#     rprint("\njoined_original_toclinks\n", joined_original_toclinks)
#     rprint("\njoined_md_toclinks\n", joined_md_toclinks)
#     print("\n\n")

#     mdtext_replacedtoc = filetext.replace(joined_original_toclinks, joined_md_toclinks)
#     print("mdtext_replacedtoc\n", mdtext_replacedtoc)

#     return toclinks_map, mdtext_replacedtoc


# def xxx(hwdoc_rpath):
#     # for hwdoc_rpath in hwdoc_rpaths:
#     hwdoc_root, hwdoc_extension = hwdoc_rpath.rsplit("/", 1)
#     rprint("\nhwdoc_rpath", hwdoc_rpath)
#     rprint("\nhwdoc_root", hwdoc_root, hwdoc_extension)
#     # if "index" in hwdoc_rpath:
#     rprint("\nhwdoc_rpath", hwdoc_rpath)
#     filetext = hfile.read_file_2string(filepath=hwdoc_rpath)
#     # rprint("\nfiletext: %s", filetext)
#     rprint("\n\n")

#     toc_list = extract_lines_between_tags(filetext=filetext)
#     toc_list_clean = clean_rst_toc_list(toc_list)
#     rprint("\ntoc_list: %s", toc_list)
#     print("toc_list_clean", toc_list_clean)

#     toclinks_map, md_toclink_list = gen_markdown_toclinks(
#         toc_list_clean=toc_list_clean, toc_root=hwdoc_root
#     )
#     print("md_toclink_list", md_toclink_list)

#     joined_original_toclinks = "\n".join(toc_list)
#     joined_md_toclinks = "\n".join(md_toclink_list)
#     rprint("\njoined_original_toclinks\n", joined_original_toclinks)
#     rprint("\njoined_md_toclinks\n", joined_md_toclinks)
#     print("\n\n")

#     mdtext_replacedtoc = filetext.replace(joined_original_toclinks, joined_md_toclinks)
#     print("mdtext_replacedtoc\n", mdtext_replacedtoc)

#     return toclinks_map, mdtext_replacedtoc


###########
def gen_ref_sub_tuplist(mdtext, ref_patt, toclinks_map):
    """
    Generates a list of tuples for ref sub.

    Args:
        mdtext (str): The text with replaced table of contents links.
        ref_patt (re.Pattern): The compiled regular expression pattern for refs.
        toclinks_map (dict): The dictionary of table of contents links.

    Returns:
        list: The list of tuples for ref sub.
    """

    ref_sub_tuplist = []
    for line in mdtext.split("\n"):
        if "{ref}" in line:
            ref_match = re.search(ref_patt, line)
            if ref_match:
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

                if toclinks_map.get(toc_link_key) is None:
                    print(f"ERROR: toc_link_key not found: {toc_link_key}")
                    print("toclinks_map keys", toclinks_map.keys())
                    sys.exit(42)
                else:
                    toc_link_value = toclinks_map[toc_link_key]
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


if __name__ == "__main__":
    ref_patt = re.compile(r"({ref})(`[a-zA-Z0-9-. ]*)(<[a-zA-Z`]*>`)")
    leftover_path = re.compile(r"^\([a-z.A-Z0-9]*\)=$")

    toclinks_map_all = {}
    mdtext_replacedtoc_data1_list_all = []
    mdtext_replacedtoc_data2_tuples_all = []

    ############
    hwdoc_rpaths = hfile.multiglob_dir_search(
        search_path="./docs_bash-it/docs/docshw/",
        glob_patt_list=["*.md"],
    )
    rprint("hwdoc_rpaths: %s", hwdoc_rpaths)

    for hwdoc_rpath in hwdoc_rpaths:
        hwdoc_root, hwdoc_extension = hwdoc_rpath.rsplit("/", 1)
        rprint("\n\n########################################################")
        rprint("########################################################")
        rprint("\nhwdoc_rpath", hwdoc_rpath)
        rprint("\nhwdoc_root, hwdoc_extension =", hwdoc_root, hwdoc_extension)

        filetext = hfile.read_file_2string(filepath=hwdoc_rpath)
        toc_list = extract_lines_between_tags(filetext=filetext)
        toc_list_clean = clean_rst_toc_list(toc_list)

        rprint("\ntoc_list: %s", toc_list)
        print("toc_list_clean", toc_list_clean)
        # if len(toc_list) > 0:
        #     sys.exit(42)

        toclinks_map, md_toclink_list = gen_markdown_toclinks(
            toc_list_clean=toc_list_clean, toc_root=hwdoc_root
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
        # toclinks_map, mdtext_replacedtoc = convert_rst_2markdown_toclinks(
        #     hwdoc_rpath=hwdoc_rpath
        # )
        toclinks_map_all.update(toclinks_map)
        mdtext_replacedtoc_data1_list_all.append(mdtext_replacedtoc)

        print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")

    for toclink_key, toclink_val in toclinks_map_all.items():
        print("   >>", toclink_key + ":\t", toclink_val)
    # sys.exit(42)

    for hwdoc_rpath in hwdoc_rpaths:
        # need toclinks_map_all, mdtext_replacedtoc
        ref_sub_tuplist = gen_ref_sub_tuplist(
            mdtext=mdtext_replacedtoc,
            ref_patt=ref_patt,
            toclinks_map=toclinks_map_all,
        )
        mdtext_replacedtoc_data2_tuples_all.append(
            (mdtext_replacedtoc, ref_sub_tuplist)
        )
        # sys.exit(42)

    ####################################################
    print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
    ### This stuff can aonly be done after getting full toclinks_map_all
    for mdtext_replacedtoc, ref_sub_tuplist in mdtext_replacedtoc_data2_tuples_all:
        mdtext_replacedrefs = replace_refs_with_links(
            mdtext=mdtext_replacedtoc, ref_sub_tuplist=ref_sub_tuplist
        )
        print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
        print("mdtext_replacedrefs\n", mdtext_replacedrefs)

        # mdtext_replacedrefs = replace_refs_with_links(
        #     mdtext=mdtext_replacedtoc, ref_sub_tuplist=ref_sub_tuplist
        # )

        # print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
        # print("mdtext_replacedrefs\n", mdtext_replacedrefs)

        # hfile.write_string_2file("./docs_bash-it/docs/docshw/index.md", mdtext_replacedrefs)
        hfile.write_string_2file("./test.md", mdtext_replacedrefs)

    # leftover_path_sub_tuplist = []
    # for line in mdtext_replacedrefs.split("\n"):
    #     if "{ref}" in line:
    #         ref_match = re.search(ref_patt, line)
    #         if ref_match:
    #             # ref_anchor = ref_match.group(1).strip()
    #             ref_title = ref_match.group(2).replace("`", "").strip()
    #             toc_link_key = (
    #                 ref_match.group(3)
    #                 .replace("`", "")
    #                 .replace("<", "")
    #                 .replace(">", "")
    #                 .strip()
    #             )
    #             rst_ref_string = (
    #                 f"{ref_match.group(1)}{ref_match.group(2)}{ref_match.group(3)}"
    #             )
