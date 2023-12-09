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


def recursively_search_dir_with_globs(search_path, glob_patt_list):
    absolute_path_list = []
    for glob_patt in glob_patt_list:
        absolute_path_list.extend(
            files_and_dirs_recursive_lister(mypathstr=search_path, myglob=glob_patt)
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


def generate_output_reldir_and_filename(file_relpath, shell_glob_patterns, replace_str):
    """
    Generates the relative path of the output directory and the output filename.

    Args:
        file_relpath (str): The relative path of the file.
        shell_glob_patterns (list): The list of shell glob patterns.
        replace_str (str): The string to replace in the filename.

    Returns:
        tuple: The relative path of the output directory and the output filename.

    Example:
        outdir_relpath, outfilename = generate_output_reldir_and_filename(
            "src/main.py", ["*.py"], ".md"
        )
    """
    filepath_split = file_relpath.split("/")
    filename = filepath_split.pop()
    output_directory_relpath = "/".join(filepath_split)

    output_file_name = str_multi_replace(
        input_str=filename,
        rm_patt_list=shell_glob_patterns,
        replace_str=replace_str,
    )

    LOG.debug("shell_glob_patterns: %s", shell_glob_patterns)
    LOG.debug("filepath_split: %s", filepath_split)
    LOG.debug(
        "output_directory_relpath: %s",
        output_directory_relpath,
    )
    LOG.debug("output_file_name: %s", output_file_name)
    LOG.debug("source_file_relative_path: %s", file_relpath)

    return output_directory_relpath, output_file_name


def generate_output_reldir_and_filename(file_relpath, glob_patterns, replace_str):
    """
    Generates the relative path of the output directory and the output filename.

    Args:
        file_relpath (str): The relative path of the file.
        glob_patterns (list): The list of shell glob patterns.
        replace_str (str): The string to replace in the filename.

    Returns:
        tuple: The file path split, the relative path of the output directory,
        and the output filename.

    Example:
        file_path_split, output_directory_path, output_filename =
        generate_output_reldir_and_filename("src/main.py", ["*.py"], ".md")
    """
    file_path_split = file_relpath.split("/")
    file_name = file_path_split.pop()
    outdir_relpath = "/".join(file_path_split)

    output_file_name = str_multi_replace(
        input_str=file_name,
        rm_patt_list=glob_patterns,
        replace_str=replace_str,
    )

    LOG.debug("glob_patterns: %s", glob_patterns)
    LOG.debug("file_path_split: %s", file_path_split)
    LOG.debug(
        "outdir_relpath: %s",
        outdir_relpath,
    )
    LOG.debug("output_file_name: %s", output_file_name)
    LOG.debug("file_relpath: %s", file_relpath)

    return file_path_split, outdir_relpath, output_file_name


def generate_category_and_output_filepath(
    category_names,
    source_file_path_parts,
    output_directory_relpath,
    output_file_name,
    undefined_category_relpath,
):
    """
    Generates the category name and the relative path of the output file.

    Args:
        category_names (list): The list of desired category names.
        source_file_path_parts (list): The list of parts of the source file path.
        output_directory_relpath (str): The relative path of the output directory.
        output_file_name (str): The name of the output file.
        undefined_category_relpath (str): The relative path of the undefined category.

    Returns:
        tuple: The category name and the relative path of the output file.
    """
    for category_name in category_names:
        if category_name in source_file_path_parts:
            category_directory_relpath = f"{output_directory_relpath}/{category_name}"
            mkdir_if_notexists(target=category_directory_relpath)
            output_file_relpath = f"{category_directory_relpath}/{output_file_name}"
            LOG.debug("output_file_relpath: %s", output_file_relpath)

            return (category_name, output_file_relpath)

    return ("undef", f"{undefined_category_relpath}/{output_file_name}")
