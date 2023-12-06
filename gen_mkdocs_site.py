"""
This module contains the GenMkdocsSite class which is used to generate a
MkDocs site. It is the main entry point for the code in this repo.
"""

import argparse
import logging
import os
import sys

from bashautodoc.helpo import hfile
from bashautodoc.helpo.coloured_log_formatter import ColouredLogFormatter
from bashautodoc.helpo.hstrops import false_when_str_contains_pattern
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
        self.build_serve = build_serve
        self.check_singlefile = check_singlefile
        self.debug = debug

        LOG.info("Loading config: %s", site_confname)
        self.conf = hfile.load_yaml_file2dict(file_name=site_confname)

        LOG.info("conf: %s", self.conf)

        self.glob_patt_list = self.conf.get("shell_glob_patterns")

        if self.glob_patt_list is None:
            self.glob_patt_list = ["*.sh"]
            self.conf["shell_glob_patterns"] = ["*.sh"]

        LOG.info("Using shell_glob_patterns: %s", self.glob_patt_list)

        ### Set paths
        self.program_root_dir = os.path.abspath(".")
        # TODO: allow project_dir to be initiated anywhere
        self.project_dir = os.path.abspath(self.conf.get("project_name"))
        self.project_docs_dir = f"{self.project_dir}/docs"
        self.project_css_dir = f"{self.project_docs_dir}/custom_css/"

        self.conf["project_docs_dir"] = self.project_docs_dir
        self.conf["project_css_dir"] = self.project_css_dir

        LOG.info("program_root_dir: %s", self.program_root_dir)
        LOG.info("project_dir: %s", self.project_dir)
        LOG.info("project_docs_dir: %s", self.project_docs_dir)
        LOG.info("project_css_dir: %s", self.project_css_dir)

    def dprint(self, myvar):
        """
        Print debug information if self.debug is True.

        Args:
            myvar (Any): The variable to print.
        """
        if self.debug:
            print(f"{myvar = }")
            print("👉", locals())

    def clean_infiles(self, infiles):
        strict_exclude_patterns = [
            f"/{patt}/" for patt in self.conf.get("exclude_patterns")
        ]

        LOG.debug("strict_exclude_patterns: %s", strict_exclude_patterns)
        cleaned_infiles = [
            infile
            for infile in infiles
            if false_when_str_contains_pattern(
                input_str=infile.replace(self.project_docs_dir, ""),
                input_patt_li=strict_exclude_patterns,
            )
        ]
        return cleaned_infiles

    def setup_docs_project(self):
        """
        Set up the docs project by copying shell source files and custom CSS
        to the project directory.
        """
        hfile.rmdir_if_exists(target=self.project_docs_dir)
        hfile.mkdir_if_notexists(target=self.project_docs_dir)

        hfile.copy_dir(
            source="custom_assets/custom_css",
            target=f"{self.project_css_dir}",
        )
        hfile.copy_dir(
            source=f'{self.conf.get("shell_srcdir")}', target=self.project_docs_dir
        )

    def create_mkdocs_site(self):
        """
        Create a MkDocs site by copying additional markdown files and generating mkdocs yaml.
        """
        LOG.info("Copying additional markdown files")
        for mdsrc, mddest in self.conf.get("additional_mdfiles").items():
            hfile.copy_file(source=mdsrc, target=f"{self.project_docs_dir}/{mddest}")

        LOG.info("Generating markdown yaml")
        yaml_dict = {
            "site_name": self.conf.get("site_name"),
            "site_url": self.conf.get("site_url"),
            "repo_url": self.conf.get("repo_url"),
            "site_author": self.conf.get("site_author"),
            # "validation": [
            #     {"omitted_files": "warn"},
            #     {"absolute_links": "warn"},
            #     {"unrecognized_links": "warn"},
            # ],
            "nav": [
                {"Home": "index.md"},
            ],
            "theme": {
                "name": "windmill-dark",
                "navigation_depth": 5,
                "highlightjs": True,
                "hljs_languages": ["bash", "python"],
            },
            "extra_css": ["custom_css/extra.css"],
        }

        for catname in self.conf.get("category_names"):
            catname_holder = []

            mdinfiles = hfile.files_and_dirs_recursive_lister(
                mypathstr=self.project_docs_dir, myglob="*.md"
            )

            LOG.debug("mdinfiles: %s", mdinfiles)

            for md_filepath in mdinfiles:
                print("catname", catname)
                print("md_filepath", md_filepath)
                if f"/{catname}/" in md_filepath:
                    print("TRUE\n")
                    page_name = md_filepath.replace(".md", "").split("/")[-1]
                    md_rel_filepath = md_filepath.replace(self.project_docs_dir, ".")
                    page_path_map = {page_name: md_rel_filepath}
                    catname_holder.append(page_path_map)

            yaml_dict["nav"].append({catname: catname_holder})

        LOG.info("Writing mkdocs config yaml")
        hfile.dict2_yaml_file(
            file_name=f"{self.project_dir}/mkdocs.yml",
            yaml_dict=yaml_dict,
        )
        # sys.exit(42)

    def main_routine(self):
        """
        Main routine for setting up the docs project, processing shell files, and creating the MkDocs site.
        """
        self.setup_docs_project()

        os.chdir(self.project_dir)

        if self.check_singlefile is None:
            infiles = []
            for glob_patt in self.glob_patt_list:
                infiles.extend(
                    hfile.files_and_dirs_recursive_lister(
                        mypathstr=self.project_docs_dir, myglob=glob_patt
                    )
                )
        else:
            LOG.warning("Checking single file")
            infiles = [self.check_singlefile]

        LOG.debug("infiles: %s", infiles)

        cleaned_infiles = self.clean_infiles(infiles)
        LOG.info("cleaned_infiles: %s", cleaned_infiles)
        # sys.exit(42)

        shell_src_preprocessor = ShellSrcPreProcessor(
            self.conf,
            cleaned_infiles,
            self.project_docs_dir,
            debug=self.debug,
        )
        shell_src_preprocessor.main_routine()

        self.create_mkdocs_site()

        if self.build_serve:
            LOG.warning("Building and serving local docs site")
            os.chdir(self.project_dir)
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
    #     dest="exclude_patterns",
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
