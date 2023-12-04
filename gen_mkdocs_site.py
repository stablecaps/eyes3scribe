"""
This module contains the GenMkdocsSite class which is used to generate a
MkDocs site. It is the main entry point for the code in this repo.
"""

import argparse
import logging
import os
import sys

from autodocumatix.helpo import hfile
from autodocumatix.helpo.coloured_log_formatter import ColouredLogFormatter
from autodocumatix.helpo.hstrops import false_when_str_contains_pattern
from autodocumatix.shell_src_preprocessor import ShellSrcPreProcessor

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

    def __init__(self, site_confname, debug=False):
        """
        Initialize the GenMkdocsSite class.

        Args:
            site_confname (str): The name of the site configuration.
            debug (bool, optional): If True, debug information will be printed. Defaults to False.
        """
        self.debug = debug

        LOG.info("Loading config: %s", site_confname)
        self.cnf = hfile.load_yaml_file2dict(file_name=site_confname)

        LOG.info("cnf: %s", self.cnf)

        ### Set paths
        self.program_root_dir = os.path.abspath(".")
        # TODO: allow project_dir to be initiated anywhere
        self.project_dir = os.path.abspath(self.cnf.get("project_name"))
        self.project_docs_dir = f"{self.project_dir}/docs"
        self.project_css_dir = f"{self.project_docs_dir}/custom_css/"

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
            f"/{patt}/" for patt in self.cnf.get("exclude_patterns")
        ]

        LOG.debug("strict_exclude_patterns: %s", strict_exclude_patterns)
        cleaned_infiles = [
            infile
            for infile in infiles
            if false_when_str_contains_pattern(
                test_str=infile.replace(self.project_docs_dir, ""),
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
            source=f'{self.cnf.get("shell_srcdir")}', target=self.project_docs_dir
        )

    def create_mkdocs_site(self):
        """
        Create a MkDocs site by copying additional markdown files and generating mkdocs yaml.
        """
        LOG.info("Copying additional markdown files")
        for mdsrc, mddest in self.cnf.get("additional_mdfiles").items():
            hfile.copy_file(source=mdsrc, target=f"{self.project_docs_dir}/{mddest}")

        LOG.info("Generating markdown yaml")
        yaml_dict = {
            "site_name": self.cnf.get("site_name"),
            "site_url": self.cnf.get("site_url"),
            "repo_url": self.cnf.get("repo_url"),
            "site_author": self.cnf.get("site_author"),
            "validation": [
                {"omitted_files": "warn"},
                {"absolute_links": "warn"},
                {"unrecognized_links": "warn"},
            ],
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

        for catname in self.cnf.get("category_names"):
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
                    md_rel_filepath = md_filepath.replace(self.project_docs_dir, "./")
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

        glob_patt_list = (
            self.cnf.get("shell_glob_patterns")
            if self.cnf.get("shell_glob_patterns")
            else ["*.sh"]
        )
        LOG.info("Using shell_glob_patterns: %s", glob_patt_list)

        infiles = []
        for glob_patt in glob_patt_list:
            infiles.extend(
                hfile.files_and_dirs_recursive_lister(
                    mypathstr=self.project_docs_dir, myglob=glob_patt
                )
            )
        LOG.debug("infiles: %s", infiles)

        cleaned_infiles = self.clean_infiles(infiles)
        LOG.warning("cleaned_infiles: %s", cleaned_infiles)

        shell_src_preprocessor = ShellSrcPreProcessor(
            cleaned_infiles,
            self.project_docs_dir,
            debug=self.debug,
        )
        shell_src_preprocessor.main_routine()

        self.create_mkdocs_site()


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
        "-d",
        "--debug",
        dest="debug",
        help="Turn debug logging on",
        type=bool,
        default=False,
        required=False,
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
    gen_mkdocs_site = GenMkdocsSite(site_confname=args.site_confname, debug=args.debug)
    gen_mkdocs_site.main_routine()

    LOG.info("Program Finished")
