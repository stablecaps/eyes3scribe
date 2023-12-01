import os
import sys
import logging
import yaml
import shutil
import argparse
import textwrap
from autodocumatix.helpo import hfile

# TODO: sort out imports better for rich print
from autodocumatix.main import ShellSrcProcessor

LOG = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, stream=sys.stdout)
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
        self.PROJECT_DIR = os.path.abspath(self.cnf["project_name"])
        self.PROJECT_DOCS_DIR = f"{self.PROJECT_DIR}/docs"
        self.PROJECT_CSS_DIR = f"{self.PROJECT_DIR}/custom_css/"
        self.OUT_DIR = self.cnf["out_dir"]

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
        hfile.mkdir_if_notexists(target=self.OUT_DIR)

        hfile.copy_dir(
            source="custom_assets/custom_css",
            target=f"{self.PROJECT_CSS_DIR}",
        )
        hfile.copy_dir(
            source=f'{self.cnf["shell_src_dir"]}', target=self.PROJECT_DOCS_DIR
        )

    def process_shell_files(self, infiles):
        shell_src_processor = ShellSrcProcessor(
            infiles, self.OUT_DIR, self.cnf["exclude_patterns"], debug=self.debug
        )

        shell_src_processor.main_routine()

    def create_mkdocs_site(self):
        LOG.info("Copying additional markdown files")
        for mdsrc, mddest in self.cnf["additional_mdfiles"].items():
            hfile.copy_file(source=mdsrc, target=f"{self.OUT_DIR}/{mddest}")

        LOG.info("Generating markdown yaml")

        # mkdocs_yml = textwrap.dedent(
        #     f"""
        # site_name: {self.cnf['site_name']}
        # site_url: {self.cnf['site_url']}
        # repo_url: {self.cnf['repo_url']}
        # site_author: {self.cnf['site_author']}
        # nav:
        #     - Home: index.md
        # """
        # )
        yaml_dict = (
            {
                "site_name": {self.cnf["site_name"]},
                "site_url": {self.cnf["site_url"]},
                "repo_url": {self.cnf["repo_url"]},
                "site_author": {self.cnf["site_author"]},
                "validation": [
                    {"omitted_files": "warn"},
                    {"absolute_links": "warn"},
                    {"unrecognized_links": "warn"},
                ],
                "nav": [
                    {"Home": "index.md"},
                ],
            },
        )

        # "validation:
        # omitted_files: warn
        # absolute_links: warn
        # unrecognized_links: warn
        for catname in self.cnf["category_names"]:
            # mkdocs_yml += f"  - {catname}:\n"
            # yaml_dict["nav"][""]

            catname_holder = []

            mdinfiles = hfile.files_and_dirs_recursive_lister(
                mypathstr=self.OUT_DIR, myglob="*.md"
            )

            print("mdinfiles", mdinfiles)
            # sys.exit(42)

            for md_filepath in mdinfiles:
                if catname in md_filepath:
                    page_name = md_filepath.replace("md.", "").split("/")[-1]
                    # mkdocs_yml += f"    {page_name}: {md_filepath}\n"
                    page_path_map = {page_name, md_filepath}
                    catname_holder.append(page_path_map)

        print()
        print(yaml_dict)
        print()

        hfile.dump_yaml_file(
            file_name=f"{self.PROJECT_DIR}/mkdocs.yml",
            yaml_string=mkdocs_yml,
        )

    def main_routine(self):
        self.setup_docs_project()

        ###
        ### Dynamically generate mkdocs.yml
        os.chdir(self.PROJECT_DIR)

        infiles = hfile.files_and_dirs_recursive_lister(
            mypathstr=self.PROJECT_DOCS_DIR, myglob="*.sh"
        )
        # print("infiles", infiles)

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

    # PROGRAM_ROOT_DIR = os.path.abspath(".")
    # print("PROGRAM_ROOT_DIR", PROGRAM_ROOT_DIR)

    # ### Load config
    # cnf = hfile.load_yaml_file2dict(file_name="config/bashrc_stablecaps.yaml")
    # print("cnf", cnf)

    # # TODO: allow PROJECT_DIR to be initiated anywhere
    # PROJECT_DIR = os.path.abspath(cnf["project_name"])
    # PROJECT_DOCS_DIR = f"{PROJECT_DIR}/docs"
    # print("PROJECT_DIR", PROJECT_DIR)
    # print("PROJECT_DOCS_DIR", PROJECT_DOCS_DIR)

    # ### Copy shell source files to project directory
    # hfile.rmdir_if_exists(target=PROJECT_DOCS_DIR)
    # hfile.mkdir_if_notexists(target=PROJECT_DOCS_DIR)

    # hfile.copy_dir(
    #     source="custom_assets/custom_css", target=f"{PROJECT_DOCS_DIR}/custom_css/"
    # )
    # hfile.copy_dir(source=f'{cnf["md_src_dir"]}', target=PROJECT_DOCS_DIR)

    # ###
    # ### Dynamically generate mkdocs.yml
    # os.chdir(PROJECT_DIR)

    # mkdocs_yml = f"""
    # site_name: {cnf['site_name']}
    # site_url: {cnf['site_url']}
    # repo_url: {cnf['repo_url']}
    # site_author: {cnf['site_author']}
    # nav:
    #     - Home: index.md
    # """

    # hfile.dump_yaml_file(
    #     file_name=f"{PROJECT_DIR}/mkdocs.yml",
    #     yaml_string=mkdocs_yml,
    # )

    # out_dir = f"{PROGRAM_ROOT_DIR}/gbm-docs"
    # exclude_patterns = "zsdoc", "test", "theme_settings_BACKUP"

    # infiles = hfile.files_and_dirs_recursive_lister(
    #     mypathstr=PROJECT_DOCS_DIR, myglob="*.sh"
    # )
    # # print("infiles", infiles)

    # shell_src_processor = ShellSrcProcessor(
    #     infiles, out_dir, exclude_patterns, debug=True
    # )

    # shell_src_processor.main_routine()

    ### Create markdown files
    # python src/main.py --infiles $(find /home/bsgt/sys_bashrc/ -name "*.sh")  \
    # --out-dir `pwd`/gbm-docs \
    # --exclude-files "zsdoc" "test" "theme_settings_BACKUP" "unused_scrap_functions"
