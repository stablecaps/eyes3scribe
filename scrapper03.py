import logging
import re
from collections import defaultdict

from rich import print as rprint

from eyes3scribe.helpo import hfile, hstrops

LOG = logging.getLogger(__name__)


mdlink_patt = re.compile(r"[- ]*\[([*a-zA-Z0-9-_]*)\]\(([A-Za-z/-0-9_.]*)")


def gen_cleaned_mdtoc_list(toc_mdlist):
    clean_toc_mdlist = []
    for line in toc_mdlist:
        line_stripped = line.strip()
        if "## Table of Contents" in line_stripped:
            pass
        elif line_stripped == "":
            pass
        else:
            mdlink_match = re.search(mdlink_patt, line_stripped)
            if mdlink_match:
                mdlink = mdlink_match.group(2)
                # rprint("mdlink", mdlink)
                # sys.exit(42)
                clean_toc_mdlist.append(mdlink)
    return clean_toc_mdlist


if __name__ == "__main__":
    ### For every mdfile
    # 1. establish if it has a TOC
    # 2. Map the hierarchy of nav-doc links via the TOC
    # 3. We will use the anchor "## Table of Contents" to find md TOC

    # hwdoc_rpaths = hfile.multiglob_dir_search(
    #     search_path="./docs_bash-it/docs/docshw/",
    #     glob_patt_list=["*.md"],
    # )

    mdtoc_path_list = hfile.flatten_list(
        nested_list=hfile.find_files_with_grep_patt(
            search_path="docs_bash-it/docs/docshw/",
            file_glob="*.md",
            txt_pattern="## Table of Contents",
        )
    )
    rprint("mdtoc_path_list", mdtoc_path_list)

    toc_mdlist_dict = {}
    for mdtoc_path in mdtoc_path_list:
        rprint("\nmdtoc_path", mdtoc_path)

        filetext = hfile.read_file_2string(filepath=mdtoc_path)
        # rprint("\nfiletext", filetext)
        # sys.exit(42)

        toc_mdlist = hstrops.get_lines_between_tag_and_blank_line(
            filetext, start_tag="## Table of Contents"
        )
        rprint("toc_mdlist", toc_mdlist)

        toc_mdlist_dict[mdtoc_path] = gen_cleaned_mdtoc_list(toc_mdlist=toc_mdlist)

    print("\n\n")
    ## 1. Check which mdtoc_path is in which list to figure out rough order
    ## 2. If it is in the list, then it is suboridnate
    ## 3. Create ranked order of mdfiles
    toc_thing_dict = defaultdict(list)
    toc_hierarchy = []
    for mdtoc_path, toclink_paths in toc_mdlist_dict.items():
        rprint("  1>>", mdtoc_path, toclink_paths)

        for mdtoc_path2, toclink_paths2 in toc_mdlist_dict.items():
            if mdtoc_path in toclink_paths2:
                rprint("  2>>", mdtoc_path2, "is in", mdtoc_path)
                toc_thing_dict[mdtoc_path2].append(mdtoc_path)
                break

    # toc_thing_dict["dummy_test"] = ["dummy_test1", "dummy_test2"]
    print("\n\ntoc_thing_dict")
    for key, value in toc_thing_dict.items():
        print("xx", key, value)

    #################
    print("\n\nConstruct name_this_better_dict")
    ### test list length
    name_this_better_dict = {}
    for key, link_list in sorted(
        toc_thing_dict.items(), key=lambda x: len(x[1]), reverse=True
    ):
        print("*", key, link_list)

        ### assume that the first one is the parent toc
        name_this_better_dict[key] = toc_mdlist_dict[key]
        # rprint("name_this_better_dict", name_this_better_dict)
        new_link_list = []
        for mdlink in name_this_better_dict[key]:
            rprint("mdlink", mdlink)
            if mdlink in link_list:
                category_split = mdlink.split("/")
                # category_rootdir = category_split[0:-2]
                if category_split[-1] == "index.md":
                    category_name = category_split[-2]
                else:
                    category_name = category_split[-1]
                subdict = {category_name: toc_mdlist_dict[mdlink]}
                new_link_list.append(subdict)
            else:
                new_link_list.append(mdlink)
        name_this_better_dict[key] = new_link_list

    rprint("name_this_better_dict", name_this_better_dict)

    # https://realpython.com/directory-tree-generator-python/
