import logging
import os
import pathlib
import shutil
import sys

import yaml

LOG = logging.getLogger(__name__)


def load_yaml_file2dict(file_name):
    """
    Load a YAML file and return its contents.

    Args:
        file_name (str): The name of the file to load.

    Returns:
        dict: The contents of the YAML file.
    """
    with open(file_name, "r", encoding="iso-8859-1") as my_yaml:
        yaml_data = yaml.safe_load(my_yaml)
        LOG.info("yaml_data: %s", yaml_data)

    return yaml_data


def dump_yaml_file(
    file_name,
    yaml_string,
):
    """
    Writes data to a YAML file.

    Args:
        file_name (str): The name of the file to write to.
        data (dict): The data to write to the file.

    Returns:
        None
    """
    yaml_data = yaml.safe_load(yaml_string)
    with open(file_name, "w") as my_yaml:
        print("Writing yaml data to file name", file_name)
        LOG.debug("yaml_data: %s", yaml_data)
        yaml.dump(yaml_data, my_yaml)


def dict2_yaml_file(
    file_name,
    yaml_dict,
):
    with open(file_name, "w") as my_yaml:
        print("Writing yaml data to file name", file_name)
        LOG.debug("yaml_dict: %s", yaml_dict)
        yaml.dump(yaml_dict, my_yaml)


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


def files_and_dirs_lister(mypathstr="./", mode="file", suf_pre="", exclude_list=None):
    """
    Lists files and directories based on the provided mode.

    Args:
        mypathstr (str, optional): The directory to search. Defaults to "./".
        mode (str, optional): The mode to use for listing ("folder", "file", "suffix", "prefix"). Defaults to "file".
        suf_pre (str, optional): The suffix or prefix to filter by. Only used if mode is "suffix" or "prefix". Defaults to "".
        exclude_list (list, optional): A list of files or directories to exclude. Defaults to [].

    Returns:
        list: A list of all matching files or directories.

    Examples:
        >>> hfile.files_and_dirs_lister(mypathstr="./", mode="file", suf_pre="", exclude_list=[])
        >>> hfile.files_and_dirs_lister(mypathstr="./", mode="folder", suf_pre="", exclude_list=[])
        >>> hfile.files_and_dirs_lister(mypathstr="./", mode="suffix", suf_pre=".sh", exclude_list=[])
        >>> hfile.files_and_dirs_lister(mypathstr="./", mode="prefix", suf_pre="gen_", exclude_list=[])
    """
    if exclude_list is None:
        exclude_list = []
      
    if mode == "folder":
        os_object_list = [
            object
            for object in os.listdir(mypathstr)
            if os.path.isdir(object)
            if object not in exclude_list
        ]

    elif mode == "file":
        os_object_list = [
            object
            for object in os.listdir(mypathstr)
            if os.path.isfile(object)
            if object not in exclude_list
        ]

    elif mode == "suffix":
        os_object_list = [
            object
            for object in os.listdir(mypathstr)
            if object.endswith(suf_pre)
            if object not in exclude_list
        ]

    elif mode == "prefix":
        os_object_list = [
            object
            for object in os.listdir(mypathstr)
            if object.startswith(suf_pre)
            if object not in exclude_list
        ]

    else:
        LOG.critical("Incorrect mode: %s", mode)

        sys.exit(0)

    return os_object_list


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
