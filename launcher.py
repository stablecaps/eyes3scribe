"""
This module contains the Launcher class which is used to generate a
MkDocs site. It is the main entry point for the code in this repo.
"""

import sentry_sdk

from bashautodoc.config import Config
from bashautodoc.setup_docs_project import SetupDocsProject

sentry_sdk.init(
    dsn="https://4b9aa1ef8464e2e3522cc9dc3d4b5a19@o4506486318563328.ingest.sentry.io/4506486328655872",
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
    enable_tracing=True,
)

import argparse
import logging
import os
import sys

# TODO: sort out import Dotmap
from dotmap import DotMap
from rich import print as rprint

from bashautodoc.create_handwritten_docs import CreateHandwrittenDocs
from bashautodoc.helpo import hfile
from bashautodoc.helpo.coloured_log_formatter import ColouredLogFormatter
from bashautodoc.shell_src_preprocessor import ShellSrcPreProcessor

LOG = logging.getLogger(__name__)
# logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

ch.setFormatter(ColouredLogFormatter())

LOG.addHandler(ch)

# 1. copy bash src files to a temp directory
# 2. copy custom css assets to appropriate place
# 3. create mkdocs.yml file
# 4. find (filter appropriate markdown files)
# 5. add to mkdocs.yml file
# 6. subprocess mkdocs build


class Launcher:
    """
    The Launcher class takes a site configuration name and an optional
    debug flag as input. It provides methods to set up the docs project,
    process shell files, and create the MkDocs site.
    """

    def __init__(self, site_confname, build_serve, check_singlefile, debug=False):
        """
        Initialize the Launcher class.

        Args:
            site_confname (str): The name of the site configuration.
            build_serve (bool): Whether to build and serve the local MkDocs site.
            check_singlefile (str): The path of a single shell source file to debug.
            debug (bool, optional): If True, debug information will be printed. Defaults to False.
        """
        # self.site_confname = site_confname
        self.build_serve = build_serve
        self.check_singlefile = check_singlefile
        self.debug = debug

        self.cnf = Config(site_confname)

        LOG.info("conf: %s", self.cnf)

        self.yaml_dict = {}
        for key, value in self.cnf.items():
            if key not in self.cnf.bashautodoc_keys:
                if isinstance(value, DotMap):
                    self.yaml_dict[key] = value.toDict()
                else:
                    self.yaml_dict[key] = value

        rprint("self.yaml_dict", self.yaml_dict)
        # sys.exit(42)

        # TODO: sort out this hacky code
        self.yaml_dict["navdict"] = {"nav": []}

    # def setup_docs_project(self):
    #     """
    #     Set up the docs project by copying shell source files and custom CSS
    #     to the project directory.
    #     """
    #     hfile.rmdir_if_exists(target=self.cnf.project_docs_dir)
    #     hfile.mkdir_if_notexists(target=self.cnf.project_docs_dir)

    #     ### make undefined category directory
    #     hfile.mkdir_if_notexists(target=self.cnf.undef_category_dir)
    #     hfile.mkdir_if_notexists(target=self.cnf.undef_category_dir_hwdocs)

    #     hfile.copy_dir(
    #         source="custom_assets/custom_css",
    #         target=self.cnf.project_css_dir,
    #     )
    #     hfile.copy_dir(source=self.cnf.shell_srcdir, target=self.cnf.project_docs_dir)

    #     # TODO: sort this out later
    #     LOG.info("Copying additional markdown files")
    #     # for mdsrc, mddest in self.classmethod"additional_mdfiles").items():
    #     #     hfile.copy_file(source=mdsrc, target=f"{self.cnf.project_docs_dir}/{mddest}")

    #     if self.cnf.handwritten_docs_dir:
    #         hfile.copy_dir(
    #             source=self.cnf.handwritten_docs_dir,
    #             target=self.cnf.handwritten_docs_outdir,
    #         )

    def mkdocs_add_handwrittendocs_to_nav(self):
        create_hwdocs = CreateHandwrittenDocs(
            cnf=self.cnf, handwritten_docs_dir=self.cnf.handwritten_docs_outdir
        )
        catname_2mdfile_dict = create_hwdocs.create_hwdocs()
        rprint("catname_2mdfile_dict", catname_2mdfile_dict)

        # self.yaml_dict["nav"].append(catname_2mdfile_dict)
        self.yaml_dict["navdict"].update(catname_2mdfile_dict)
        rprint("self.yaml_dict['navdict']", self.yaml_dict["navdict"])
        # sys.exit(42)
        self.yaml_dict["nav"] = self.yaml_dict["navdict"]["nav"]

        rprint("\n\nself.yaml_dict['nav']", self.yaml_dict["nav"])
        # sys.exit(42)

        del self.yaml_dict["navdict"]

        # TODO: fix hacky copy/replace docs dir

        # sys.exit(42)
        hfile.rmdir_if_exists(target="docs_bash-it/docs_temp")
        hfile.move_files_and_dirs(
            source="docs_bash-it/docs/docshw", target="docs_bash-it/docs_temp"
        )
        hfile.move_files_and_dirs(
            source="docs_bash-it/docs/custom_css", target="docs_bash-it/custom_css_temp"
        )
        # sys.exit(42)
        hfile.rmdir_if_exists(target="docs_bash-it/docs")
        hfile.move_files_and_dirs(
            source="docs_bash-it/docs_temp", target="docs_bash-it/docs"
        )
        hfile.move_files_and_dirs(
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
        # ) = hfile.get_src_reldir_and_filename(
        #     file_rpath=docfile_rpath,
        #     glob_patterns=self.classmethod"docs_glob_patterns"),
        #     replace_str=".md",
        # )

        # LOG.debug("docfilename: %s", docfilename)
        # LOG.debug("docfilename_noext: %s", docfilename_noext)
        # sys.exit(42)

        # # TODOD: change docfilename --> docfilename_noext
        # self.yaml_dict["nav"].append({docfilename: docfile_rpath})

    def mkdocs_add_srcdocs_to_nav(self, catname_2mdfile_dict):
        rprint("catname_2mdfile_dict", catname_2mdfile_dict)
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
        rprint("catname_2mdfile_dict", sorted(catname_2mdfile_dict["undef"]))
        # sys.exit(42)

        srcdoc_dict = {"nav": [{"Reference": []}]}
        for catname in self.cnf.catnames_src:
            print("catname", catname)
            cat_mdoutfiles_rpaths = sorted(catname_2mdfile_dict.get(catname))
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

    def gen_mkdocs_yaml(self, catname_2mdfile_dict):
        """
        Create a MkDocs site by copying additional markdown files and generating mkdocs yaml.
        """

        LOG.info("Set generated src docs to nav")
        self.mkdocs_add_srcdocs_to_nav(catname_2mdfile_dict)

        if self.cnf["handwritten_docs_dir"]:
            LOG.info("Set handwritten docs as main to nav")
            self.mkdocs_add_handwrittendocs_to_nav()

        import yaml

        LOG.debug("self.yaml_dict: %s", yaml.safe_dump(self.yaml_dict))
        # sys.exit(42)

        LOG.info("Writing mkdocs config yaml")

        hfile.dict2_yaml_file(
            filename=f"{self.cnf.project_reldir}/mkdocs.yml",
            yaml_dict=self.yaml_dict,
        )
        # sys.exit(42)

    def main(self):
        """
        Main routine for setting up the docs project, processing shell files, and creating the MkDocs site.
        """

        setup_docs_project = SetupDocsProject(
            cnf=self.cnf, check_singlefile=self.check_singlefile
        )
        rpaths = setup_docs_project.main()

        clean_hwdocs_rpaths = rpaths["clean_hwdocs_rpaths"]
        clean_srcfiles_rpaths = rpaths["clean_srcfiles_rpaths"]

        ###########################self.mkdocs_add_srcdocs_to_nav(self, catname_2mdfile_dict)

        shell_src_preprocessor = ShellSrcPreProcessor(
            self.cnf,
            clean_srcfiles_rpaths,
            self.cnf.project_docs_dir,
            debug=self.debug,
        )
        catname_2mdfile_dict = shell_src_preprocessor.run()

        self.gen_mkdocs_yaml(catname_2mdfile_dict)

        if self.build_serve:
            LOG.warning("Building and serving local docs site")
            os.chdir(self.cnf.project_reldir)
            # TODO: use subprocess
            os.system("mkdocs build")
            os.system("mkdocs serve")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Gen-Bash-MkDoc",
        usage="python launcher.py --site-confname config/bashrc_stablecaps.yaml",
    )

    parser.add_argument(
        "-s",
        "--site-confname",
        dest="site_confname",
        help="Location of Site conf in yaml format",
        type=str,
        default=None,
        required=True,
    )

    parser.add_argument(
        "-b",
        "---build-serve",
        dest="build_serve",
        help="Build & Serve local mkdocs site after generating docs site",
        action="store_true",
    )

    parser.add_argument(
        "-c",
        "--check-singlefile",
        dest="check_singlefile",
        help="Pass the path of a single shell src file to debug",
        type=str,
        default=None,
        required=False,
    )

    parser.add_argument(
        "-d", "--debug", dest="debug", help="Turn debug logging on", action="store_true"
    )

    args = parser.parse_args()
    launcher = Launcher(
        site_confname=args.site_confname,
        build_serve=args.build_serve,
        check_singlefile=args.check_singlefile,
        debug=args.debug,
    )
    launcher.main()

    LOG.info("Program Finished")
