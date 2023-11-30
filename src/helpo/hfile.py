import os
import sys
import logging
import yaml
import shutil

LOG = logging.getLogger(__name__)


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
