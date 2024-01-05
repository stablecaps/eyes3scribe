import logging
import os
import sys

import yaml
from rich import print as rprint

from bashautodoc.helpo.hfile import (
    copy_dir,
    mkdir_if_notexists,
    move_files_and_dirs,
    rmdir_if_exists,
    write_dict_2yaml_file,
)

LOG = logging.getLogger(__name__)


class GenMkdocsSiteYaml:
    def __init__(self, cnf, catname_2mdfile_dict, navbar_cleaned_dict, yaml_dict):
        self.cnf = cnf
        self.catname_2mdfile_dict = catname_2mdfile_dict
        self.navbar_cleaned_dict = navbar_cleaned_dict
        self.yaml_dict = yaml_dict
        self.yaml_dict["navdict"] = {"nav": []}

    def mkdocs_add_handwrittendocs_to_nav(self):
        # self.yaml_dict["nav"].append(catname_2mdfile_dict)
        self.yaml_dict["navdict"].update(self.navbar_cleaned_dict)
        rprint("self.yaml_dict['navdict']", self.yaml_dict["navdict"])
        # sys.exit(42)
        self.yaml_dict["nav"] = self.yaml_dict["navdict"]["nav"]

        rprint("\n\nself.yaml_dict['nav']", self.yaml_dict["nav"])
        # sys.exit(42)

        del self.yaml_dict["navdict"]

        # TODO: fix hacky copy/replace docs dir

        # sys.exit(42)
        rmdir_if_exists(target="docs_bash-it/docs_temp")
        move_files_and_dirs(
            source="docs_bash-it/docs/docshw", target="docs_bash-it/docs_temp"
        )
        move_files_and_dirs(
            source="docs_bash-it/docs/custom_css", target="docs_bash-it/custom_css_temp"
        )
        # sys.exit(42)
        rmdir_if_exists(target="docs_bash-it/docs")
        move_files_and_dirs(source="docs_bash-it/docs_temp", target="docs_bash-it/docs")
        move_files_and_dirs(
            source="docs_bash-it/custom_css_temp", target="docs_bash-it/docs/custom_css"
        )

        # sys.exit(42)

        # for catname in ["docshw"]:  # self.classmethod"catnames_docs"):
        #     LOG.debug("catname: %s", catname)

        #     cat_mdoutfiles_rpaths = sorted(catname_2mdfile_dict.get(catname))
        #     catname_holder = []
        #     for mdoutfile_rpath in cat_mdoutfiles_rpaths:
        #         print("catname", catname)
        #         print("mdoutfile_rpath", mdoutfile_rpath)
        #         page_name = mdoutfile_rpath.replace(".md", "").split("/")[-1]
        #         mdoutfile_routepath = mdoutfile_rpath.replace(
        #             f"{self.cnf.project_docs_dir}", "."
        #         )
        #         print("self.cnf.project_docs_dir", self.cnf.project_docs_dir)
        #         print("mdoutfile_routepath", mdoutfile_routepath)
        #         # sys.exit(42)
        #         page_path_map = {page_name: mdoutfile_routepath}
        #         catname_holder.append(page_path_map)

        # ###########################################
        # srcdocs_parent = None
        # if srcdocs_parent is None:
        #     self.yaml_dict["nav"].append({catname: catname_holder})
        # else:
        #     self.yaml_dict["nav"][1][srcdocs_parent].append(
        #         {catname: catname_holder}
        #     )

        # (
        #     docfile_path_split,
        #     docoutdir_rpath,
        #     docfilename,
        # ) = get_src_reldir_and_filename(
        #     file_rpath=docfile_rpath,
        #     glob_patterns=self.classmethod"docs_glob_patterns"),
        #     replace_str=".md",
        # )

        # LOG.debug("docfilename: %s", docfilename)
        # LOG.debug("docfilename_noext: %s", docfilename_noext)
        # sys.exit(42)

        # # TODOD: change docfilename --> docfilename_noext
        # self.yaml_dict["nav"].append({docfilename: docfile_rpath})

    def mkdocs_add_srcdocs_to_nav(self):
        rprint("catname_2mdfile_dict", self.catname_2mdfile_dict)
        # sys.exit(42)

        # TODO: re-enable optional srcdocs nesting once things are refactored
        # ref_or_main_raw = self.classmethod"nav_codedocs_as_ref_or_main")
        # ref_or_main = ref_or_main_raw if ref_or_main_raw else "main"

        # nav_codedocs_name_raw = self.classmethod"nav_codedocs_name")
        # nav_codedocs_name = (
        #     nav_codedocs_name_raw if self.classmethod"nav_codedocs_name") else "Code-Docs"
        # )

        # if ref_or_main == "main":
        #     srcdocs_parent = None
        # elif ref_or_main == "ref":
        #     self.yaml_dict["nav"].append({nav_codedocs_name: []})
        #     srcdocs_parent = nav_codedocs_name
        # else:
        #     LOG.error(
        #         "Error: nav_codedocs_as_ref_or_main must be set to either 'main' or 'ref'"
        #     )
        #     sys.exit(42)

        LOG.info("Add generated code docs to nav")
        rprint("catname_2mdfile_dict", sorted(self.catname_2mdfile_dict["undef"]))
        # sys.exit(42)

        srcdoc_dict = {"nav": [{"Reference": []}]}
        for catname in self.cnf.catnames_src:
            print("catname", catname)
            cat_mdoutfiles_rpaths = sorted(self.catname_2mdfile_dict.get(catname))
            catname_holder = []

            for mdoutfile_rpath in cat_mdoutfiles_rpaths:
                print("catname", catname)
                print("mdoutfile_rpath", mdoutfile_rpath)
                page_name = mdoutfile_rpath.replace(".md", "").split("/")[-1]
                mdoutfile_routepath = mdoutfile_rpath.replace(
                    f"{self.cnf.project_docs_dir}", "."
                )
                print("self.cnf.project_docs_dir", self.cnf.project_docs_dir)
                print("mdoutfile_routepath", mdoutfile_routepath)
                # sys.exit(42)
                page_path_map = {page_name: mdoutfile_routepath}
                catname_holder.append(page_path_map)

            # rprint("self.yaml_dict[", self.yaml_dict)
            # if srcdocs_parent is None:
            #     self.yaml_dict["nav"].append({catname: catname_holder})
            # else:
            #     self.yaml_dict["nav"][1][srcdocs_parent].append(
            #         {catname: catname_holder}
            #     )
            srcdoc_dict["nav"].append({catname: catname_holder})

        rprint("\n\navdict", self.yaml_dict["navdict"])
        rprint("\n\nsrcdoc_dict", srcdoc_dict)

        self.yaml_dict["navdict"].update(srcdoc_dict)

        rprint("\n\nnavdict2", self.yaml_dict["navdict"])
        # sys.exit(42)

    def main(self):
        if self.cnf["handwritten_docs_dir"]:
            LOG.info("Set handwritten docs as main to nav")
            self.mkdocs_add_handwrittendocs_to_nav()

        # LOG.info("Set generated src docs to nav")
        # self.mkdocs_add_srcdocs_to_nav()

        LOG.debug("self.yaml_dict: %s", yaml.safe_dump(self.yaml_dict))

        LOG.info("Writing mkdocs config yaml")
        write_dict_2yaml_file(
            filename=f"{self.cnf.project_reldir}/mkdocs.yml",
            yaml_dict=self.yaml_dict,
        )
