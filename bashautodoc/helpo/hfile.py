import logging
import os
import pathlib
import shutil
import sys

from ruamel.yaml import YAML

# import yaml


LOG = logging.getLogger(__name__)

yaml = YAML(typ="safe")


def load_yaml_file2dict(file_name):
    """
    Load a YAML file into a dictionary.

    Args:
        file_name (str): The name of the YAML file.

    Returns:
        dict: The loaded YAML data.

    Example:
        yaml_data = load_yaml_file2dict("config.yaml")
    """
    with open(file_name, "r", encoding="iso-8859-1") as yaml_path:
        yaml_data = yaml.load(yaml_path)
        LOG.info("yaml_data: %s", yaml_data)
    return yaml_data


def dump_yaml_file(
    file_name,
    yaml_string,
):
    """
    Dump a YAML string into a file.

    Args:
        file_name (str): The name of the file to write to.
        yaml_string (str): The YAML string to write.

    Example:
        dump_yaml_file("config.yaml", "key: value")
    """
    yaml_data = yaml.load(yaml_string)
    with open(file_name, "w") as yaml_path:
        print("Writing yaml data to file name", file_name)
        LOG.debug("yaml_data: %s", yaml_data)
        yaml.dump(yaml_data, yaml_path)


def dict2_yaml_file(
    file_name,
    yaml_dict,
):
    """
    Write a dictionary to a file in YAML format.

    Args:
        file_name (str): The name of the file to write to.
        yaml_dict (dict): The dictionary to write.

    Example:
        dict2_yaml_file("config.yaml", {"key": "value"})
    """
    with open(file_name, "w") as yaml_path:
        print("Writing yaml data to file name", file_name)
        LOG.debug("yaml_dict: %s", yaml_dict)
        yaml.dump(yaml_dict, yaml_path)


def rmdir_if_exists(target):
    """
    Remove a directory if it exists.

    Args:
        target (str): The directory to remove.
    """
    ...

    if os.path.exists(target):
        print("Deleting Directory:", target)
        shutil.rmtree(target)


def mkdir_if_notexists(target):
    """
    Create a directory if it does not exist.

    Args:
        target (str): The directory to create.
    """
    if not os.path.exists(target):
        print("Making Directory:", target)
        os.makedirs(target)


def copy_clobber(source, target):
    rmdir_if_exists(target)

    shutil.copytree(source, target)

    LOG.info("Copied: %s --> %s", source, target)


def copy_dir(source, target):
    shutil.copytree(source, target, dirs_exist_ok=True)

    LOG.info("Copied: %s --> %s", source, target)


def copy_file(source, target):
    """
    Copies a directory from source to target.

    Args:
        source (str): The source directory to copy.
        target (str): The target directory to copy to.
    Exanple:
        >>> hfile.copy_dir(source="custom_assets/custom_css", target=f"{project_docs_dir}/custom_css/")
    """
    shutil.copyfile(source, target)

    LOG.info("Copied: %s --> %s", source, target)


def files_and_dirs_recursive_lister(mypathstr="./", myglob="*.sh"):
    """
    Lists all files in a directory and its subdirectories that match a given glob.

    Args:
        mypathstr (str, optional): The directory to search. Defaults to "./".
        myglob (str, optional): The glob to match files against. Defaults to "*.sh".

    Returns:
        list: A list of all matching files.

    Example:
            >>> files_and_dirs_recursive_lister(mypathstr="/home/user", myglob="*.txt")
    """
    mypath = pathlib.Path(mypathstr)

    file_list = [
        object.as_posix() for object in mypath.rglob(myglob) if object.is_file()
    ]

    return file_list
