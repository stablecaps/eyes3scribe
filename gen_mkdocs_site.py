"""
This module contains the GenMkdocsSite class which is used to generate a
MkDocs site. It is the main entry point for the code in this repo.
"""

import argparse
import logging
import os
import sys

from rich import print as rprint

from bashautodoc.create_handwritten_docs import CreateHandwrittenDocs
from bashautodoc.helpo import hfile
from bashautodoc.helpo.coloured_log_formatter import ColouredLogFormatter
from bashautodoc.helpo.hstrops import str_multi_replace
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


class GenMkdocsSite:
    """
    The GenMkdocsSite class takes a site configuration name and an optional
    debug flag as input. It provides methods to set up the docs project,
    process shell files, and create the MkDocs site.
    """

    def __init__(self, site_confname, build_serve, check_singlefile, debug=False):
        """
        Initialize the GenMkdocsSite class.

        Args:
            site_confname (str): The name of the site configuration.
            build_serve (bool): Whether to build and serve the local MkDocs site.
            check_singlefile (str): The path of a single shell source file to debug.
            debug (bool, optional): If True, debug information will be printed. Defaults to False.
        """
        self.site_confname = site_confname
        self.build_serve = build_serve
        self.check_singlefile = check_singlefile
        self.debug = debug

        LOG.info("Loading config: %s", self.site_confname)
        self.conf = hfile.load_yaml_file2dict(filename=site_confname)
        self.check_config()

        LOG.info("conf: %s", self.conf)

        self.shell_glob_patterns = self.conf.get("shell_glob_patterns")
        if self.shell_glob_patterns is None:
            self.shell_glob_patterns = ["*.sh"]
            self.conf["shell_glob_patterns"] = ["*.sh"]

        self.docs_glob_patterns = self.conf.get("docs_glob_patterns")
        if self.docs_glob_patterns is None:
            self.shell_glob_patterns = ["*.md"]
            self.conf["shell_gldocs_glob_patternsob_patterns"] = ["*.md"]

        LOG.info("Using shell_glob_patterns: %s", self.shell_glob_patterns)
        LOG.info("Using docs_glob_patterns: %s", self.docs_glob_patterns)

        ### Set paths
        self.program_root_dir = os.path.abspath(".")
        # TODO: allow project_reldir to be initiated anywhere
        self.project_name = self.conf.get("project_name")
        self.project_absdir = os.path.abspath(self.project_name)
        self.project_reldir = f"{os.path.relpath(self.project_name)}"
        self.project_docs_dir = f"{self.project_reldir}/docs"
        self.project_css_dir = f"{self.project_docs_dir}/custom_css/"
        self.undef_category_dir = f"{self.project_docs_dir}/undef"
        self.undef_category_dir_hwdocs = f"{self.project_docs_dir}/docshw/undef"
        self.handwritten_docs_dir = self.conf["handwritten_docs_dir"]
        self.handwritten_docs_outdir = f"./{self.project_docs_dir}/docshw"

        self.exclusion_patterns_src = self.conf.get("exclusion_patterns_src")
        self.exclusion_patterns_docs = self.conf.get("exclusion_patterns_docs")

        self.conf["program_root_dir"] = self.program_root_dir
        self.conf["project_reldir"] = self.project_reldir
        self.conf["project_docs_dir"] = self.project_docs_dir
        self.conf["project_css_dir"] = self.project_css_dir
        self.conf["undef_category_dir"] = self.undef_category_dir
        self.conf["undef_category_dir_hwdocs"] = self.undef_category_dir_hwdocs

        self.conf["catnames_src"].append("undef")
        self.conf["catnames_docs"].append("undef")

        self.conf_bashautodoc_keys = [
            "project_name",
            "program_root_dir",
            "project_reldir",
            "project_docs_dir",
            "project_css_dir",
            "undef_category_dir",
            "undef_category_dir_hwdocs",
            "shell_srcdir",
            "shell_glob_patterns",
            "exclusion_patterns_src",
            "additional_mdfiles",
            "catnames_src",
            "catnames_docs",
            "nav_codedocs_as_ref_or_main",
            "nav_codedocs_name",
            "handwritten_docs_dir",
            "docs_glob_patterns",
            "exclusion_patterns_docs",
            "rst2myst_configfile",
        ]

        self.conf["func_def_keywords"] = [
            "about",
            "group",
            "param",
            "example",
        ]

        self.yaml_dict = {
            key: value
            for (key, value) in self.conf.items()
            if key not in self.conf_bashautodoc_keys
        }

        LOG.info("project_name: %s", self.project_name)
        LOG.info("program_root_dir: %s", self.program_root_dir)
        LOG.info("project_reldir: %s", self.project_reldir)
        LOG.info("project_docs_dir: %s", self.project_docs_dir)
        LOG.info("project_css_dir: %s", self.project_css_dir)
        LOG.info("undef_category_dir: %s", self.undef_category_dir)
        LOG.info(
            "undef_category_dir_hwdocs: %s",
            self.undef_category_dir_hwdocs,
        )

        LOG.info("handwritten_docs_dir: %s", self.handwritten_docs_dir)
        LOG.info("handwritten_docs_outdir: %s", self.handwritten_docs_outdir)
        LOG.info("exclusion_patterns_src: %s", self.exclusion_patterns_src)
        LOG.info("exclusion_patterns_docs: %s", self.exclusion_patterns_docs)

        self.exclusion_patterns_docs

    def check_config(self):
        """
        Check the configuration for errors.
        """
        LOG.info("Checking config...")

        expected_keys = {
            "project_name": None,
            "site_name": None,
            "site_url": None,
            "site_author": None,
            "repo_url": None,
            "nav": None,
            "shell_srcdir": None,
            "catnames_src": None,
            "nav_codedocs_as_ref_or_main": ["ref", "main"],
        }

        current_conf_keys = list(self.conf.keys())

        for ckey in list(expected_keys.keys()):
            cvalue = self.conf.get(ckey)
            if ckey not in current_conf_keys:
                LOG.error(
                    "Error: Missing key <%s> in config file: <%s>\nExiting..",
                    ckey,
                    self.site_confname,
                )
                sys.exit(42)

            expected_key_value = expected_keys.get(ckey)

            if isinstance(expected_key_value, list):
                if cvalue not in expected_key_value:
                    LOG.error(
                        "Error: Key <%s> in config file: <%s> has unexpected value <%s>\nOptions are: <%s>\nExiting..",
                        ckey,
                        self.site_confname,
                        cvalue,
                        expected_key_value,
                    )
                    sys.exit(42)

            if self.conf.get(ckey) is None:
                LOG.error(
                    "Error: Key <%s> in config file: <%s> has no value\nExiting..",
                    ckey,
                    self.site_confname,
                )
                sys.exit(42)

    def setup_docs_project(self):
        """
        Set up the docs project by copying shell source files and custom CSS
        to the project directory.
        """
        hfile.rmdir_if_exists(target=self.project_docs_dir)
        hfile.mkdir_if_notexists(target=self.project_docs_dir)

        ### make undefined category directory
        hfile.mkdir_if_notexists(target=self.undef_category_dir)
        hfile.mkdir_if_notexists(target=self.undef_category_dir_hwdocs)

        hfile.copy_dir(
            source="custom_assets/custom_css",
            target=f"{self.project_css_dir}",
        )
        hfile.copy_dir(
            source=f'{self.conf.get("shell_srcdir")}', target=self.project_docs_dir
        )

        LOG.info("Copying additional markdown files")
        for mdsrc, mddest in self.conf.get("additional_mdfiles").items():
            hfile.copy_file(source=mdsrc, target=f"{self.project_docs_dir}/{mddest}")

        if self.handwritten_docs_dir is not None:
            hfile.copy_dir(
                source=f'{self.conf.get("handwritten_docs_dir")}',
                target=self.handwritten_docs_outdir,
            )

    def mkdocs_add_handwrittendocs_to_nav(self):
        create_hwdocs = CreateHandwrittenDocs(
            conf=self.conf, handwritten_docs_dir=self.handwritten_docs_outdir
        )
        catname_2mdfile_dict = create_hwdocs.create_hwdocs()
        rprint("catname_2mdfile_dict", catname_2mdfile_dict)

        self.yaml_dict["nav"].append(catname_2mdfile_dict)
        # sys.exit(42)

        # for catname in ["docshw"]:  # self.conf.get("catnames_docs"):
        #     LOG.debug("catname: %s", catname)

        #     cat_mdoutfiles_rpaths = sorted(catname_2mdfile_dict.get(catname))
        #     catname_holder = []
        #     for mdoutfile_rpath in cat_mdoutfiles_rpaths:
        #         print("catname", catname)
        #         print("mdoutfile_rpath", mdoutfile_rpath)
        #         page_name = mdoutfile_rpath.replace(".md", "").split("/")[-1]
        #         mdoutfile_routepath = mdoutfile_rpath.replace(
        #             f"{self.project_docs_dir}", "."
        #         )
        #         print("self.project_docs_dir", self.project_docs_dir)
        #         print("mdoutfile_routepath", mdoutfile_routepath)
        #         # sys.exit(42)
        #         page_path_map = {page_name: mdoutfile_routepath}
        #         catname_holder.append(page_path_map)

        # ###########################################
        # code_docs_parent = None
        # if code_docs_parent is None:
        #     self.yaml_dict["nav"].append({catname: catname_holder})
        # else:
        #     self.yaml_dict["nav"][1][code_docs_parent].append(
        #         {catname: catname_holder}
        #     )

        # (
        #     docfile_path_split,
        #     docoutdir_rpath,
        #     docfilename,
        # ) = hfile.get_src_reldir_and_filename(
        #     file_rpath=docfile_rpath,
        #     glob_patterns=self.conf.get("docs_glob_patterns"),
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

        ref_or_main_raw = self.conf.get("nav_codedocs_as_ref_or_main")
        ref_or_main = ref_or_main_raw if ref_or_main_raw else "main"

        nav_codedocs_name_raw = self.conf.get("nav_codedocs_name")
        nav_codedocs_name = (
            nav_codedocs_name_raw if self.conf.get("nav_codedocs_name") else "Code-Docs"
        )

        if ref_or_main == "main":
            code_docs_parent = None
        elif ref_or_main == "ref":
            self.yaml_dict["nav"].append({nav_codedocs_name: []})
            code_docs_parent = nav_codedocs_name
        else:
            LOG.error(
                "Error: nav_codedocs_as_ref_or_main must be set to either 'main' or 'ref'"
            )
            sys.exit(42)

        LOG.info("Add generated code docs to nav")
        rprint("catname_2mdfile_dict", sorted(catname_2mdfile_dict["undef"]))
        # sys.exit(42)

        for catname in self.conf.get("catnames_src"):
            print("catname", catname)
            cat_mdoutfiles_rpaths = sorted(catname_2mdfile_dict.get(catname))
            catname_holder = []

            for mdoutfile_rpath in cat_mdoutfiles_rpaths:
                print("catname", catname)
                print("mdoutfile_rpath", mdoutfile_rpath)
                page_name = mdoutfile_rpath.replace(".md", "").split("/")[-1]
                mdoutfile_routepath = mdoutfile_rpath.replace(
                    f"{self.project_docs_dir}", "."
                )
                print("self.project_docs_dir", self.project_docs_dir)
                print("mdoutfile_routepath", mdoutfile_routepath)
                # sys.exit(42)
                page_path_map = {page_name: mdoutfile_routepath}
                catname_holder.append(page_path_map)

            if code_docs_parent is None:
                self.yaml_dict["nav"].append({catname: catname_holder})
            else:
                self.yaml_dict["nav"][1][code_docs_parent].append(
                    {catname: catname_holder}
                )

    def create_mkdocs_yaml(self, catname_2mdfile_dict):
        """
        Create a MkDocs site by copying additional markdown files and generating mkdocs yaml.
        """

        LOG.info("Set generated src docs to nav")
        self.mkdocs_add_srcdocs_to_nav(catname_2mdfile_dict)

        if self.conf["handwritten_docs_dir"] is not None:
            LOG.info("Set handwritten docs as main to nav")
            self.mkdocs_add_handwrittendocs_to_nav()

        import yaml

        LOG.debug("self.yaml_dict: %s", yaml.safe_dump(self.yaml_dict))
        # sys.exit(42)

        LOG.info("Writing mkdocs config yaml")
        hfile.dict2_yaml_file(
            filename=f"{self.project_reldir}/mkdocs.yml",
            yaml_dict=self.yaml_dict,
        )
        # sys.exit(42)

    def main(self):
        """
        Main routine for setting up the docs project, processing shell files, and creating the MkDocs site.
        """
        self.setup_docs_project()

        # TODO: sort out using arbitrary directory
        # os.chdir(self.project_reldir)

        if self.handwritten_docs_dir is not None:
            LOG.info("Processing handwritten doc files")
            hwdocs_rpaths = hfile.multiglob_dir_search(
                search_path=self.handwritten_docs_outdir,
                glob_patt_list=self.docs_glob_patterns,
            )
            LOG.debug("hwdocs_rpaths: %s", hwdocs_rpaths)

            # TODO: move exclusion_patterns_src into class init
            strict_exclusion_patterns_docs = [
                patt for patt in self.exclusion_patterns_docs
            ]
            LOG.debug(
                "strict_exclusion_patterns_docs: %s", strict_exclusion_patterns_docs
            )

            cleaned_hwdocs_rpaths = hfile.filter_paths_excluding_patterns(
                path_list=hwdocs_rpaths,
                exclusion_patterns_src=strict_exclusion_patterns_docs,
            )
            LOG.debug("cleaned_hwdocs_rpaths: %s", cleaned_hwdocs_rpaths)
            # sys.exit(42)

            # self.mkdocs_add_srcdocs_to_nav(self, catname_2mdfile_dict)

        LOG.info("Processing shell source files")
        if self.check_singlefile is None:
            src_absolute_path_list = hfile.multiglob_dir_search(
                search_path=self.project_docs_dir,
                glob_patt_list=self.shell_glob_patterns,
            )
        else:
            LOG.warning("Checking single file")
            src_absolute_path_list = [self.check_singlefile]

        LOG.debug("src_absolute_path_list: %s", src_absolute_path_list)

        # TODO: move exclusion_patterns_src into class init
        strict_exclusion_patterns_src = [
            f"/{patt}/" for patt in self.conf.get("exclusion_patterns_src")
        ]
        LOG.debug("strict_exclusion_patterns_src: %s", strict_exclusion_patterns_src)

        srcfiles_rpath = hfile.replace_substr_in_paths(
            input_paths=src_absolute_path_list,
            replace_path=self.program_root_dir,
        )
        LOG.info("srcfiles_rpath: %s", srcfiles_rpath)

        cleaned_srcfiles_rpaths = hfile.filter_paths_excluding_patterns(
            path_list=srcfiles_rpath,
            exclusion_patterns_src=strict_exclusion_patterns_src,
        )
        LOG.debug("cleaned_srcfiles_rpaths: %s", cleaned_srcfiles_rpaths)

        shell_src_preprocessor = ShellSrcPreProcessor(
            self.conf,
            cleaned_srcfiles_rpaths,
            self.project_docs_dir,
            debug=self.debug,
        )
        catname_2mdfile_dict = shell_src_preprocessor.run()

        self.create_mkdocs_yaml(catname_2mdfile_dict)

        if self.build_serve:
            LOG.warning("Building and serving local docs site")
            os.chdir(self.project_reldir)
            # TODO: use subprocess
            os.system("mkdocs build")
            os.system("mkdocs serve")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Gen-Bash-MkDoc",
        usage="python gen_mkdocs_site.py --site-confname config/bashrc_stablecaps.yaml",
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
    gen_mkdocs_site = GenMkdocsSite(
        site_confname=args.site_confname,
        build_serve=args.build_serve,
        check_singlefile=args.check_singlefile,
        debug=args.debug,
    )
    gen_mkdocs_site.main()

    LOG.info("Program Finished")
