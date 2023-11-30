import os
import sys
import logging
import yaml
import shutil

from src.helpo import hfile

LOG = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, stream=sys.stdout)
# 1. copy bash src files to a temp directory
# 2. copy custom css assets to appropriate place
# 3. create mkdocs.yml file
# 4. find (filter appropriate markdown files)
# 5. add to mkdocs.yml file
# 6. subprocess mkdocs build


if __name__ == "__main__":
    # PROGRAM_ROOT_DIR = os.path.abspath(".")
    # print("PROGRAM_ROOT_DIR", PROGRAM_ROOT_DIR)

    ### Load config
    myconf = hfile.load_yaml_file(file_name="config/bashrc_stablecaps.yaml")
    print("myconf", myconf)

    # TODO: allow PROJECT_DIR to be initiated anywhere
    PROJECT_DIR = os.path.abspath(myconf["project_name"])
    PROJECT_DOCS_DIR = f"{PROJECT_DIR}/docs"
    print("PROJECT_DIR", PROJECT_DIR)
    print("PROJECT_DOCS_DIR", PROJECT_DOCS_DIR)

    ### Copy shell source files to project directory
    hfile.rmdir_if_exists(target=PROJECT_DOCS_DIR)
    hfile.mkdir_if_notexists(target=PROJECT_DOCS_DIR)

    hfile.copy_dir(
        source="custom_assets/custom_css", target=f"{PROJECT_DOCS_DIR}/custom_css/"
    )
    hfile.copy_dir(source=f'{myconf["md_src_dir"]}', target=PROJECT_DOCS_DIR)

    ###
    ### Dynamically generate mkdocs.yml
    os.chdir(PROJECT_DIR)

    mkdocs_yml = f"""
    site_name: {myconf['site_name']}
    site_url: {myconf['site_url']}
    repo_url: {myconf['repo_url']}
    site_author: {myconf['site_author']}
    nav:
        - Home: index.md
    """

    hfile.dump_yaml_file(
        file_name=f"{PROJECT_DIR}/mkdocs.yml",
        yaml_string=mkdocs_yml,
    )

    ### Create markdown files
    # python src/main.py --infiles $(find /home/bsgt/sys_bashrc/ -name "*.sh")  \
    # --out-dir `pwd`/gbm-docs \
    # --exclude-files "zsdoc" "test" "theme_settings_BACKUP" "unused_scrap_functions"
