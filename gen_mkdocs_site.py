import os
import sys
import logging
import yaml
import shutil

LOG = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, stream=sys.stdout)
# 1. copy bash src files to a temp directory
# 2. copy custom css assets to appropriate place
# 3. create mkdocs.yml file
# 4. find (filter appropriate markdown files)
# 5. add to mkdocs.yml file
# 6. subprocess mkdocs build


def load_yaml_file(file_name):
    with open(file_name, "r", encoding="iso-8859-1") as my_yaml:
        yaml_data = yaml.safe_load(my_yaml)
        LOG.info("yaml_data: %s", yaml_data)

    return yaml_data


def dump_yaml_file(
    file_name,
    yaml_string,
):
    yaml_data = yaml.safe_load(yaml_string)
    with open(file_name, "w") as my_yaml:
        print("Writing yaml data to file name", file_name)
        LOG.info("yaml_data: %s", yaml_data)
        yaml.dump(yaml_data, my_yaml)

    return yaml_data


def rmdir_if_exists(target):
    """Remove file directory if it exists."""

    if os.path.exists(target):
        print("Deleting Directory:", target)
        shutil.rmtree(target)


def mkdir_if_notexists(target):
    """Make a file directory if it does not exist."""

    if not os.path.exists(target):
        print("Making Directory:", target)
        os.makedirs(target)


def copy_clobber(source, target):
    """Copy directory. Overwrite target folder if it exists."""

    rmdir_if_exists(target)

    shutil.copytree(source, target)

    LOG.info("Copied: %s --> %s", source, target)


def copy_dir(source, target):
    """Copy directory."""

    shutil.copytree(source, target, dirs_exist_ok=True)

    LOG.info("Copied: %s --> %s", source, target)


if __name__ == "__main__":
    # PROGRAM_ROOT_DIR = os.path.abspath(".")
    # print("PROGRAM_ROOT_DIR", PROGRAM_ROOT_DIR)

    ### Load config
    myconf = load_yaml_file(file_name="config/bashrc_stablecaps.yaml")
    print("myconf", myconf)

    # TODO: allow PROJECT_DIR to be initiated anywhere
    PROJECT_DIR = os.path.abspath(myconf["project_name"])
    PROJECT_DOCS_DIR = f"{PROJECT_DIR}/docs"
    print("PROJECT_DIR", PROJECT_DIR)
    print("PROJECT_DOCS_DIR", PROJECT_DOCS_DIR)

    ### Copy shell source files to project directory
    rmdir_if_exists(target=PROJECT_DOCS_DIR)
    mkdir_if_notexists(target=PROJECT_DOCS_DIR)

    copy_dir(
        source="custom_assets/custom_css", target=f"{PROJECT_DOCS_DIR}/custom_css/"
    )
    copy_dir(source=f'{myconf["md_src_dir"]}', target=PROJECT_DOCS_DIR)

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

    dump_yaml_file(
        file_name=f"{PROJECT_DIR}/mkdocs.yml",
        yaml_string=mkdocs_yml,
    )

    ### Create markdown files
    # python src/main.py --infiles $(find /home/bsgt/sys_bashrc/ -name "*.sh")  \
    # --out-dir `pwd`/gbm-docs \
    # --exclude-files "zsdoc" "test" "theme_settings_BACKUP" "unused_scrap_functions"
