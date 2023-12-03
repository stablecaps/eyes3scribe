import os
import sys
import logging
import yaml
import shutil
import argparse
import textwrap
from autodocumatix.helpo import hfile

# TODO: sort out imports better for rich print
from autodocumatix.shell_src_preprocessor import ShellSrcPreProcessor

LOG = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
# 1. copy bash src files to a temp directory
# 2. copy custom css assets to appropriate place
# 3. create mkdocs.yml file
# 4. find (filter appropriate markdown files)
# 5. add to mkdocs.yml file
# 6. subprocess mkdocs build


class GenMkdocsSite:
    def __init__(self, site_confname, debug=False):
        self.debug = debug

        LOG.info("Loading config: %s", site_confname)
        self.cnf = hfile.load_yaml_file2dict(file_name="config/bashrc_stablecaps.yaml")

        LOG.info("cnf: %s", self.cnf)

        ### Set paths
        self.PROGRAM_ROOT_DIR = os.path.abspath(".")
        # TODO: allow PROJECT_DIR to be initiated anywhere
        self.PROJECT_DIR = os.path.abspath(self.cnf.get("project_name"))
        self.PROJECT_DOCS_DIR = f"{self.PROJECT_DIR}/docs"
        self.PROJECT_CSS_DIR = f"{self.PROJECT_DOCS_DIR}/custom_css/"

        LOG.info("PROGRAM_ROOT_DIR: %s", self.PROGRAM_ROOT_DIR)
        LOG.info("PROJECT_DIR: %s", self.PROJECT_DIR)
        LOG.info("PROJECT_DOCS_DIR: %s", self.PROJECT_DOCS_DIR)
        LOG.info("PROJECT_CSS_DIR: %s", self.PROJECT_CSS_DIR)

    def dprint(self, myvar):
        if self.debug:
            print(f"{myvar = }")
            print("👉", locals())

    def setup_docs_project(self):
        ### Copy shell source files to project directory
        hfile.rmdir_if_exists(target=self.PROJECT_DOCS_DIR)
        hfile.mkdir_if_notexists(target=self.PROJECT_DOCS_DIR)

        hfile.copy_dir(
            source="custom_assets/custom_css",
            target=f"{self.PROJECT_CSS_DIR}",
        )
        hfile.copy_dir(
            source=f'{self.cnf.get("shell_srcdir")}', target=self.PROJECT_DOCS_DIR
        )

    def process_shell_files(self, infiles):
        shell_src_preprocessor = ShellSrcPreProcessor(
            infiles,
            self.PROJECT_DOCS_DIR,
            self.cnf.get("exclude_patterns"),
            debug=self.debug,
        )

        shell_src_preprocessor.main_routine()

    def create_mkdocs_site(self):
        LOG.info("Copying additional markdown files")
        for mdsrc, mddest in self.cnf.get("additional_mdfiles").items():
            hfile.copy_file(source=mdsrc, target=f"{self.PROJECT_DOCS_DIR}/{mddest}")

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
                mypathstr=self.PROJECT_DOCS_DIR, myglob="*.md"
            )

            print("mdinfiles", mdinfiles)

            for md_filepath in mdinfiles:
                if catname in md_filepath:
                    page_name = md_filepath.replace(".md", "").split("/")[-1]
                    md_rel_filepath = md_filepath.replace(self.PROJECT_DOCS_DIR, "./")
                    page_path_map = {page_name: md_rel_filepath}
                    catname_holder.append(page_path_map)

            yaml_dict["nav"].append({catname: catname_holder})

        LOG.info("Writing mkdocs config yaml")
        hfile.dict2_yaml_file(
            file_name=f"{self.PROJECT_DIR}/mkdocs.yml",
            yaml_dict=yaml_dict,
        )

    def main_routine(self):
        self.setup_docs_project()

        os.chdir(self.PROJECT_DIR)

        infiles = hfile.files_and_dirs_recursive_lister(
            mypathstr=self.PROJECT_DOCS_DIR, myglob="*.sh"
        )

        self.process_shell_files(infiles)

        self.create_mkdocs_site()


if __name__ == "__main__":
    help_banner = "????????????????????"

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
        nargs="*",
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
