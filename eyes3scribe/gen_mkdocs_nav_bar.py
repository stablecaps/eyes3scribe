import logging

from rich import print as rprint

from eyes3scribe.helpo.hfile import move_files_and_dirs, rmdir_if_exists

LOG = logging.getLogger(__name__)


class GenMkdocsNavBar:
    def __new__(cls, cnf, catname_2mdfile_dict, navbar_cleaned_dict):
        cls.cnf = cnf
        cls.catname_2mdfile_dict = catname_2mdfile_dict
        cls.navbar_cleaned_dict = navbar_cleaned_dict
        cls.navdict = {"nav": []}

        return cls.main()

    @classmethod
    def mkdocs_add_handwrittendocs_to_nav(cls):
        cls.navdict.update(cls.navbar_cleaned_dict)
        rprint("cls.navdict", cls.navdict)
        # sys.exit(42)

        rprint("\n\ncls.navdict['nav']", cls.navdict["nav"])
        # sys.exit(42)

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

        # for catname in ["docshw"]:  # cls.classmethod"catnames_docs"):
        #     LOG.debug("catname: %s", catname)

        #     cat_mdoutfiles_rpaths = sorted(catname_2mdfile_dict.get(catname))
        #     catname_holder = []
        #     for mdoutfile_rpath in cat_mdoutfiles_rpaths:
        #         print("catname", catname)
        #         print("mdoutfile_rpath", mdoutfile_rpath)
        #         page_name = mdoutfile_rpath.replace(".md", "").split("/")[-1]
        #         mdoutfile_routepath = mdoutfile_rpath.replace(
        #             f"{cls.cnf.project_docs_dir}", "."
        #         )
        #         print("cls.cnf.project_docs_dir", cls.cnf.project_docs_dir)
        #         print("mdoutfile_routepath", mdoutfile_routepath)
        #         # sys.exit(42)
        #         page_path_map = {page_name: mdoutfile_routepath}
        #         catname_holder.append(page_path_map)

        # ###########################################
        # srcdocs_parent = None
        # if srcdocs_parent is None:
        #     cls.yaml_dict["nav"].append({catname: catname_holder})
        # else:
        #     cls.yaml_dict["nav"][1][srcdocs_parent].append(
        #         {catname: catname_holder}
        #     )

        # (
        #     docfile_path_split,
        #     docoutdir_rpath,
        #     docfilename,
        # ) = get_src_reldir_and_filename(
        #     file_rpath=docfile_rpath,
        #     glob_patterns=cls.classmethod"docs_glob_patterns"),
        #     replace_str=".md",
        # )

        # LOG.debug("docfilename: %s", docfilename)
        # LOG.debug("docfilename_noext: %s", docfilename_noext)
        # sys.exit(42)

        # # TODOD: change docfilename --> docfilename_noext
        # cls.yaml_dict["nav"].append({docfilename: docfile_rpath})

    @classmethod
    def mkdocs_add_srcdocs_to_nav(cls):
        rprint("catname_2mdfile_dict", cls.catname_2mdfile_dict)
        # sys.exit(42)

        # TODO: re-enable optional srcdocs nesting once things are refactored
        # ref_or_main_raw = cls.classmethod"nav_codedocs_as_ref_or_main")
        # ref_or_main = ref_or_main_raw if ref_or_main_raw else "main"

        # nav_codedocs_name_raw = cls.classmethod"nav_codedocs_name")
        # nav_codedocs_name = (
        #     nav_codedocs_name_raw if cls.classmethod"nav_codedocs_name") else "Code-Docs"
        # )

        # if ref_or_main == "main":
        #     srcdocs_parent = None
        # elif ref_or_main == "ref":
        #     cls.yaml_dict["nav"].append({nav_codedocs_name: []})
        #     srcdocs_parent = nav_codedocs_name
        # else:
        #     LOG.error(
        #         "Error: nav_codedocs_as_ref_or_main must be set to either 'main' or 'ref'"
        #     )
        #     sys.exit(42)

        LOG.info("Add generated code docs to nav")
        rprint("catname_2mdfile_dict", sorted(cls.catname_2mdfile_dict["undef"]))
        # sys.exit(42)

        srcdoc_dict = {"nav": [{"Reference": []}]}
        for catname in cls.cnf.catnames_src:
            print("catname", catname)
            cat_mdoutfiles_rpaths = sorted(cls.catname_2mdfile_dict.get(catname))
            catname_holder = []

            for mdoutfile_rpath in cat_mdoutfiles_rpaths:
                print("catname", catname)
                print("mdoutfile_rpath", mdoutfile_rpath)
                page_name = mdoutfile_rpath.replace(".md", "").split("/")[-1]
                mdoutfile_routepath = mdoutfile_rpath.replace(
                    f"{cls.cnf.project_docs_dir}", "."
                )
                print("cls.cnf.project_docs_dir", cls.cnf.project_docs_dir)
                print("mdoutfile_routepath", mdoutfile_routepath)
                # sys.exit(42)
                page_path_map = {page_name: mdoutfile_routepath}
                catname_holder.append(page_path_map)

            # rprint("cls.yaml_dict[", cls.yaml_dict)
            # if srcdocs_parent is None:
            #     cls.yaml_dict["nav"].append({catname: catname_holder})
            # else:
            #     cls.yaml_dict["nav"][1][srcdocs_parent].append(
            #         {catname: catname_holder}
            #     )
            srcdoc_dict["nav"].append({catname: catname_holder})

        rprint("\n\navdict", cls.navdict)
        rprint("\n\nsrcdoc_dict", srcdoc_dict)

        cls.navdict.update(srcdoc_dict)

        rprint("\n\nnavdict2", cls.navdict)
        # sys.exit(42)

    @classmethod
    def main(cls):
        if cls.cnf["handwritten_docs_indir"]:
            LOG.info("Set handwritten docs as main to nav")
            cls.mkdocs_add_handwrittendocs_to_nav()

        # LOG.info("Set generated src docs to nav")
        # cls.mkdocs_add_srcdocs_to_nav()

        rprint("cls.navdict", cls.navdict)

        return cls.navdict
