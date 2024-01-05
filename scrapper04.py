import logging
import re
from collections import defaultdict

from rich import print as rprint

from bashautodoc.helpo import hfile, hstrops

LOG = logging.getLogger(__name__)

# TODO: initialise all regex patterns in a single place
mdlink_patt = re.compile(r"[- ]*\[([*a-zA-Z0-9-_]*)\]\(([A-Za-z/-0-9_.]*)")


class GenNavbarDict:
    def __init__(self, search_path) -> None:
        ### For every mdfile
        # 1. establish if it has a TOC
        # 2. Map the hierarchy of nav-doc links via the TOC
        # 3. We will use the anchor "## Table of Contents" to find md TOC

        self.toc_dict = {}
        self.hierarchy_dict = defaultdict(list)
        self.navbar_dict = {}

        self.mdtoc_path_list = hfile.flatten_list(
            nested_list=hfile.find_files_with_grep_patt(
                search_path=search_path,
                file_glob="*.md",
                txt_pattern="## Table of Contents",
            )
        )
        rprint("mdtoc_path_list", self.mdtoc_path_list)

    @staticmethod
    def gen_cleaned_mdtoc_list(toc_mdlist):
        clean_toc_mdlist = []
        for line in toc_mdlist:
            line_stripped = line.strip()
            if "## Table of Contents" in line_stripped:
                pass
            elif line_stripped == "":
                pass
            else:
                mdlink_match = mdlink_patt.search(line_stripped)
                if mdlink_match:
                    mdlink = mdlink_match.group(2)
                    clean_toc_mdlist.append(mdlink)
        return clean_toc_mdlist

    def gen_toc_dict_from_mdindex_files(self):
        for mdpath in self.mdtoc_path_list:
            file_text = hfile.read_file_2string(filepath=mdpath)
            table_of_contents = hstrops.get_lines_between_tag_and_blank_line(
                file_text, start_tag="## Table of Contents"
            )
            self.toc_dict[mdpath] = GenNavbarDict.gen_cleaned_mdtoc_list(
                toc_mdlist=table_of_contents
            )

    def gen_toc_hierarchy_dict(self):
        for mdpath, toc_links in self.toc_dict.items():
            for file_path2, toc_links2 in self.toc_dict.items():
                if mdpath in toc_links2:
                    self.hierarchy_dict[file_path2].append(mdpath)
                    break

    def gen_navbar_dict(self):
        for key, link_list in sorted(
            self.hierarchy_dict.items(), key=lambda x: len(x[1]), reverse=True
        ):
            self.navbar_dict[key] = self.toc_dict[key]
            new_link_list = []
            for mdlink in self.navbar_dict[key]:
                if mdlink in link_list:
                    category_split = mdlink.split("/")
                    if category_split[-1] == "index.md":
                        category_name = category_split[-2]
                    else:
                        category_name = category_split[-1]

                    yaml2_sublist = []
                    for link in self.toc_dict[mdlink]:
                        yaml2_sublist.append(
                            {link.split("/")[-1].replace(".md", ""): link}
                        )

                    sub_dict = {category_name: yaml2_sublist}
                    new_link_list.append(sub_dict)
                else:
                    # TODO: make category split a function
                    new_link_list.append(
                        {mdlink.split("/")[-1].replace(".md", ""): mdlink}
                    )
            self.navbar_dict[key] = new_link_list

    def main(self):
        self.gen_toc_dict_from_mdindex_files()

        ## 1. Check which mdtoc_path is in which list to figure out rough order
        ## 2. If it is in the list, then it is suboridnate
        ## 3. Create ranked order of mdfiles
        self.gen_toc_hierarchy_dict()

        self.gen_navbar_dict()

        rprint("navbar_dict", self.navbar_dict)


# Call the main function
if __name__ == "__main__":
    table_of_contents_processor = GenNavbarDict(search_path="docs_bash-it/docs/docshw/")
    table_of_contents_processor.main()
