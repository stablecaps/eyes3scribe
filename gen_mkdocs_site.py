"""
This module contains the GenMkdocsSite class which is used to generate a
MkDocs site. It is the main entry point for the code in this repo.
"""

import argparse
import logging
import os
import sys

from rich import print as rprint

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
        self.conf = hfile.load_yaml_file2dict(file_name=site_confname)
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
        # TODO: allow project_dir to be initiated anywhere
        self.project_name = self.conf.get("project_name")
        self.project_dir = os.path.abspath(self.project_name)
        self.project_docs_dir = f"{self.project_dir}/docs"
        self.project_css_dir = f"{self.project_docs_dir}/custom_css/"
        self.udef_category_relpath = f"{self.project_docs_dir}/undef"
        self.handwritten_docs_dir = self.conf["handwritten_docs_dir"]
        self.handwritten_docs_outdir = f"./{self.project_name}/docs/docs_hw"

        self.exclusion_patterns_src = self.conf.get("exclusion_patterns_src")
        self.exclusion_patterns_docs = self.conf.get("exclusion_patterns_docs")

        self.conf["program_root_dir"] = self.program_root_dir
        self.conf["project_dir"] = self.project_dir
        self.conf["project_docs_dir"] = self.project_docs_dir
        self.conf["project_css_dir"] = self.project_css_dir
        self.conf["udef_category_relpath"] = f"./{self.project_name}/docs/undef"
        self.conf["category_names_src"].append("undef")

        self.conf_bashautodoc_keys = [
            "project_name",
            "program_root_dir",
            "project_dir",
            "project_docs_dir",
            "project_css_dir",
            "udef_category_relpath",
            "shell_srcdir",
            "shell_glob_patterns",
            "exclusion_patterns_src",
            "additional_mdfiles",
            "category_names_src",
            "nav_codedocs_as_ref_or_main",
            "nav_codedocs_name",
            "handwritten_docs_dir",
            "docs_glob_patterns",
            "exclusion_patterns_docs",
        ]

        self.yaml_dict = {
            key: value
            for (key, value) in self.conf.items()
            if key not in self.conf_bashautodoc_keys
        }

        LOG.info("project_name: %s", self.project_name)
        LOG.info("program_root_dir: %s", self.program_root_dir)
        LOG.info("project_dir: %s", self.project_dir)
        LOG.info("project_docs_dir: %s", self.project_docs_dir)
        LOG.info("project_css_dir: %s", self.project_css_dir)
        LOG.info("udef_category_relpath: %s", self.udef_category_relpath)
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
            "category_names_src": None,
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
        hfile.mkdir_if_notexists(target=self.udef_category_relpath)

        hfile.copy_dir(
            source="custom_assets/custom_css",
            target=f"{self.project_css_dir}",
        )
        hfile.copy_dir(
            source=f'{self.conf.get("shell_srcdir")}', target=self.project_docs_dir
        )

        if self.handwritten_docs_dir is not None:
            hfile.copy_dir(
                source=f'{self.conf.get("shell_srcdir")}',
                target=self.handwritten_docs_outdir,
            )

    def mkdocs_add_handwrittendocs_to_nav(self):
        if self.conf["handwritten_docs_dir"] is None:
            pass
        else:
            handwritten_docs_infiles = hfile.recursively_search_dir_with_globs(
                mypathstr=self.handwritten_docs_outdir,
                glob_patt_list=self.docs_glob_patterns,
            )

            LOG.debug("handwritten_docs_infiles: %s", handwritten_docs_infiles)

            for mdfile in handwritten_docs_infiles:
                mdfile_relpath = mdfile.replace(self.program_root_dir, ".")
                mdfile_relpath = mdfile_relpath.replace("./", "")
                mdfile_relpath = mdfile_relpath.replace("//", "/")

                LOG.debug("mdfile_relpath: %s", mdfile_relpath)

                mdfile_name = mdfile_relpath.split("/")[-1]
                mdfile_name_noext = mdfile_name.replace(".md", "")

                LOG.debug("mdfile_name: %s", mdfile_name)
                LOG.debug("mdfile_name_noext: %s", mdfile_name_noext)

                self.yaml_dict["nav"].append({mdfile_name_noext: mdfile_relpath})

    def mkdocs_add_codedocs_to_nav(self, catname_2mdfile_dict):
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
        rprint("catname_2mdfile_dict", catname_2mdfile_dict)

        for catname in self.conf.get("category_names_src"):
            print("catname", catname)
            cat_mdoutfiles_relpaths = sorted(catname_2mdfile_dict.get(catname))
            catname_holder = []

            for mdoutfile_relpath in cat_mdoutfiles_relpaths:
                print("catname", catname)
                print("mdoutfile_relpath", mdoutfile_relpath)
                page_name = mdoutfile_relpath.replace(".md", "").split("/")[-1]
                mdoutfile_routepath = mdoutfile_relpath.replace(
                    f"./{self.project_name}/docs", "."
                )
                print("self.project_name", self.project_name)
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

    def create_mkdocs_site(self, catname_2mdfile_dict):
        """
        Create a MkDocs site by copying additional markdown files and generating mkdocs yaml.
        """
        # TODO: move Copying additional files to main routine?
        LOG.info("Copying additional markdown files")
        for mdsrc, mddest in self.conf.get("additional_mdfiles").items():
            hfile.copy_file(source=mdsrc, target=f"{self.project_docs_dir}/{mddest}")

        LOG.info("Set generated code docs as main or ref")
        self.mkdocs_add_codedocs_to_nav(catname_2mdfile_dict)

        import yaml

        LOG.debug("self.yaml_dict: %s", yaml.safe_dump(self.yaml_dict))
        # sys.exit(42)

        LOG.info("Writing mkdocs config yaml")
        hfile.dict2_yaml_file(
            file_name=f"{self.project_dir}/mkdocs.yml",
            yaml_dict=self.yaml_dict,
        )
        # sys.exit(42)

    def main_routine(self):
        """
        Main routine for setting up the docs project, processing shell files, and creating the MkDocs site.
        """
        self.setup_docs_project()

        # TODO: sort out using arbitrary directory
        # os.chdir(self.project_dir)

        if self.handwritten_docs_dir is not None:
            LOG.info("Processing handwritten doc files")
            hwdocs_relpaths = hfile.recursively_search_dir_with_globs(
                search_path=self.handwritten_docs_outdir,
                glob_patt_list=self.docs_glob_patterns,
            )
            LOG.debug("hwdocs_relpaths: %s", hwdocs_relpaths)

            # TODO: move exclusion_patterns_src into class init
            strict_exclusion_patterns_docs = [
                patt for patt in self.exclusion_patterns_docs
            ]
            LOG.debug(
                "strict_exclusion_patterns_docs: %s", strict_exclusion_patterns_docs
            )

            cleaned_hwdocs_relpaths = hfile.filter_paths_excluding_patterns(
                path_list=hwdocs_relpaths,
                exclusion_patterns_src=strict_exclusion_patterns_docs,
            )
            LOG.debug("cleaned_hwdocs_relpaths: %s", cleaned_hwdocs_relpaths)
            # sys.exit(42)

            # self.mkdocs_add_codedocs_to_nav(self, catname_2mdfile_dict)

        LOG.info("Processing shell source files")
        if self.check_singlefile is None:
            src_absolute_path_list = hfile.recursively_search_dir_with_globs(
                search_path=self.project_docs_dir,
                glob_patt_list=self.shell_glob_patterns,
            )
        else:
            LOG.warning("Checking single file")
            src_absolute_path_list = [self.check_singlefile]

        LOG.debug("src_absolute_path_list: %s", src_absolute_path_list)

        strict_exclusion_patterns_src = [
            f"/{patt}/" for patt in self.conf.get("exclusion_patterns_src")
        ]
        LOG.debug("strict_exclusion_patterns_src: %s", strict_exclusion_patterns_src)

        srcfiles_relpath = hfile.convert_paths_to_relative(
            absolute_path_list=src_absolute_path_list,
            path_to_replace=self.program_root_dir,
        )
        LOG.info("srcfiles_relpath: %s", srcfiles_relpath)

        cleaned_srcfiles_relpaths = hfile.filter_paths_excluding_patterns(
            path_list=srcfiles_relpath,
            exclusion_patterns_src=strict_exclusion_patterns_src,
        )
        LOG.debug("cleaned_srcfiles_relpaths: %s", cleaned_srcfiles_relpaths)

        shell_src_preprocessor = ShellSrcPreProcessor(
            self.conf,
            cleaned_srcfiles_relpaths,
            self.project_docs_dir,
            debug=self.debug,
        )
        catname_2mdfile_dict = shell_src_preprocessor.main_routine()

        self.create_mkdocs_site(catname_2mdfile_dict)

        if self.build_serve:
            LOG.warning("Building and serving local docs site")
            os.chdir(self.project_dir)
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

    # parser.add_argument(
    #     "-x",
    #     "--exclude-files",
    #     dest="exclusion_patterns_src",
    #     help="List of space seperated file path patterns to exclude",
    #     type=str,
    #     nargs="*",
    #     default=[],
    # )

    args = parser.parse_args()
    gen_mkdocs_site = GenMkdocsSite(
        site_confname=args.site_confname,
        build_serve=args.build_serve,
        check_singlefile=args.check_singlefile,
        debug=args.debug,
    )
    gen_mkdocs_site.main_routine()

    LOG.info("Program Finished")
