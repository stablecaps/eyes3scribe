import logging
import os
import pathlib
import shutil
import sys

from ruamel.yaml import YAML

from bashautodoc.helpo.hstrops import does_string_contain_pattern, str_multi_replace

# import yaml


LOG = logging.getLogger(__name__)

yaml = YAML(typ="safe")


def load_yaml_file2dict(filename):
    """
    Load a YAML file into a dictionary.

    Args:
        filename (str): The name of the YAML file.

    Returns:
        dict: The loaded YAML data.

    Example:
        yaml_data = load_yaml_file2dict("config.yaml")
    """
    with open(filename, "r", encoding="iso-8859-1") as yaml_path:
        yaml_data = yaml.load(yaml_path)
        LOG.info("yaml_data: %s", yaml_data)
    return yaml_data


def dump_yaml_file(
    filename,
    yaml_string,
):
    """
    Dump a YAML string into a file.

    Args:
        filename (str): The name of the file to write to.
        yaml_string (str): The YAML string to write.

    Example:
        dump_yaml_file("config.yaml", "key: value")
    """
    yaml_data = yaml.load(yaml_string)
    with open(filename, "w") as yaml_path:
        print("Writing yaml data to file name", filename)
        LOG.debug("yaml_data: %s", yaml_data)
        yaml.dump(yaml_data, yaml_path)


def dict2_yaml_file(
    filename,
    yaml_dict,
):
    """
    Write a dictionary to a file in YAML format.

    Args:
        filename (str): The name of the file to write to.
        yaml_dict (dict): The dictionary to write.

    Example:
        dict2_yaml_file("config.yaml", {"key": "value"})
    """
    with open(filename, "w") as yaml_path:
        print("Writing yaml data to file name", filename)
        LOG.debug("yaml_dict: %s", yaml_dict)
        yaml.dump(yaml_dict, yaml_path)


def read_file_2string(filepath):
    with open(filepath, "r") as infile:
        file_text = infile.read()
    return file_text


def write_string_2file(filepath, file_text):
    with open(filepath, "w") as outfile:
        LOG.debug("Writing file: %s", filepath)
        outfile.write(file_text)


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


def move_file(source, target):
    shutil.move(source, target)

    LOG.info("Moved: %s --> %s", source, target)


def list_matching_files_recursively(search_path="./", myglob="*.sh"):
    mypath = pathlib.Path(search_path)

    file_list = [
        object.as_posix() for object in mypath.rglob(myglob) if object.is_file()
    ]

    return file_list


def search_directory_with_multiple_globs(search_path, glob_patt_list):
    absolute_path_list = []
    for glob_patt in glob_patt_list:
        absolute_path_list.extend(
            list_matching_files_recursively(search_path=search_path, myglob=glob_patt)
        )

    LOG.debug("absolute_path_list: %s", absolute_path_list)
    return absolute_path_list


def convert_paths_to_relative(absolute_path_list, path_to_replace):
    relative_paths = []
    for file_abspath in absolute_path_list:
        print("file_abspath", file_abspath)

        file_relpath = file_abspath.replace(path_to_replace, ".")
        print("file_relpath", file_relpath)

        relative_paths.append(file_relpath)
    return relative_paths


def filter_paths_excluding_patterns(path_list, exclusion_patterns_src):
    LOG.debug("Exclusion patterns: %s", exclusion_patterns_src)

    filtered_paths = []
    for path in path_list:
        print("Path", path)

        if not does_string_contain_pattern(
            input_str=path,
            input_patt_li=exclusion_patterns_src,
        ):
            filtered_paths.append(path)
    return filtered_paths
