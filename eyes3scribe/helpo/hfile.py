import logging
import os
import pathlib
import shutil
from os.path import relpath

from dotmap import DotMap
from rich import print
from ruamel.yaml import YAML

import eyes3scribe.helpo.hsubprocess as hsubp
from eyes3scribe.helpo.hstrops import does_str_contain_pattern, rreplace

LOG = logging.getLogger(__name__)

yaml = YAML(typ="safe")

####################################################################
### File read & write Ops
###


def write_dict_2yaml_file(filename, yaml_dict, mode="w"):
    with open(filename, mode) as yaml_path:
        print("Writing yaml data to file name", filename)
        LOG.debug("yaml_dict: %s", yaml_dict)
        yaml.dump(yaml_dict, yaml_path)


def write_string_2file(filepath, file_text, mode="w"):
    with open(filepath, mode) as outfile:
        LOG.debug("Writing file: %s", filepath)
        outfile.write(file_text)


def write_list_2file(filepath, strlist, mode="w"):
    with open(filepath, mode) as outfile:
        LOG.debug("Writing file: %s", filepath)
        for line in strlist:
            outfile.write(line + "\n")


###
def read_file_2string(filepath, mode="r"):
    with open(filepath, mode) as infile:
        file_text = infile.read()
    return file_text


def read_file_2list(filepath, mode="r"):
    mylist = []
    with open(filepath, mode) as infile:
        for line in infile.read().split("\n"):
            if len(line) > 0:
                mylist.append(line)
    return mylist


###
def load_yaml_file2dotmap(filename, mode="r"):
    with open(filename, mode, encoding="iso-8859-1") as yaml_path:
        yaml_data = yaml.load(yaml_path)
        LOG.info("yaml_data: %s", yaml_data)
    return DotMap(yaml_data)


def dump_yaml_file(filename, yaml_string, mode="w"):
    yaml_data = yaml.load(yaml_string)
    with open(filename, mode) as yaml_path:
        print("Writing yaml data to file name", filename)
        LOG.debug("yaml_data: %s", yaml_data)
        yaml.dump(yaml_data, yaml_path)


####################################################################
### Files & Directory Ops
###


def delfiles_not_in_list(folder, exclude_list):
    """Delete all files in folder apart from those in exclude list."""
    ### prepare delete list
    del_files = os.listdir(folder)
    # TODO: this is repeated in rm_col_names (generalise)
    for excl_str in exclude_list:
        try:
            del_files.remove(excl_str)
        except (ValueError, KeyError):
            pass

    ### delete files
    for rmfile in del_files:
        file_path = os.path.join(folder, rmfile)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as err:
            print(err)


def rmfile_if_exists(target):
    #  so we should check if file exists or not not before deleting them
    if os.path.exists(target):
        os.remove(target)
        return True

    LOG.warning("Delete file attempt failed for %s", target)
    return False


def rmdir_if_exists(target):
    if os.path.exists(target):
        print("Deleting Directory:", target)
        shutil.rmtree(target)


def mkdir_if_notexists(target):
    if not os.path.exists(target):
        print("Making Directory:", target)
        os.makedirs(target)


def copy_clobber(source, target):
    rmdir_if_exists(target)

    shutil.copytree(source, target)

    LOG.info("Copied: %s --> %s", source, target)


def copy_dir(source, target, symlinks=False, dirs_exist_ok=True):
    shutil.copytree(source, target, symlinks=symlinks, dirs_exist_ok=dirs_exist_ok)

    LOG.info("Copied: %s --> %s", source, target)


def copy_file(source, target):
    shutil.copyfile(source, target)

    LOG.info("Copied: %s --> %s", source, target)


def move_files_and_dirs(source, target):
    shutil.move(source, target)

    LOG.info("Moved: %s --> %s", source, target)


####################################################################
### Search & Filter Ops
###
def list_matching_files_recursively(search_path="./", myglob="*.sh"):
    mypath = pathlib.Path(search_path)

    file_list = [
        object.as_posix() for object in mypath.rglob(myglob) if object.is_file()
    ]

    return file_list


def multiglob_dir_search(search_path, glob_patt_list):
    path_list = []
    for glob_patt in glob_patt_list:
        path_list.extend(
            list_matching_files_recursively(search_path=search_path, myglob=glob_patt)
        )

    LOG.debug("path_list: %s", path_list)
    return path_list


def replace_substr_in_paths(input_paths, replace_path):
    relative_paths = []
    for filepath in input_paths:
        print("filepath", filepath)

        replaced_path = filepath.replace(replace_path, ".")
        print("replaced_path", replaced_path)

        relative_paths.append(replaced_path)
    return relative_paths


# TODO: similart to clean_list_via_rm_patts in hstrops
def filter_paths_excluding_patterns(path_list, exclusion_patterns_src):
    LOG.debug("Exclusion patterns: %s", exclusion_patterns_src)

    filtered_paths = []
    for path in path_list:
        print("Path", path)

        if not does_str_contain_pattern(
            instr=path,
            input_patt_li=exclusion_patterns_src,
        ):
            filtered_paths.append(path)
    return filtered_paths


def find_files_with_grep_patt(search_path, file_glob, txt_pattern):
    comm = (
        f'find {search_path} -not -path "*/\.*" -not -path "*venv/*" -not -path "*node_modules/*" -iname "{file_glob}" -exec grep --color=never -Isl "{txt_pattern}"'
        + " {} /dev/null \;"
    )
    resp_bytes = hsubp.run_cmd_with_output(comm_str=comm)
    print("resp_bytes", resp_bytes)

    resp_list = hsubp.process_subp_output(cmd_output=resp_bytes, delimiter="\n")
    return resp_list


def get_relative_path_between_files(end_filepath, start_filepath):
    # TODO: test this to make sure it handles edge cases properly
    # TODO: refactor this to be less ugly
    start2child_relpath_raw = relpath(end_filepath, start_filepath)
    start2child_relpath = rreplace(
        mystr=start2child_relpath_raw, match_str="../", replace_str="", times=1
    )

    if start2child_relpath == ".":
        start2child_relpath = ""

    return start2child_relpath
