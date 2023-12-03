import pytest
import os
import tempfile

from autodocumatix.helpo.hfile import (
    load_yaml_file2dict,
    dump_yaml_file,
    rmdir_if_exists,
    mkdir_if_notexists,
    copy_clobber,
    copy_dir,
    copy_file,
)


def test_load_yaml_file2dict():
    # Create a temporary yaml file
    with tempfile.NamedTemporaryFile(suffix=".yaml", delete=False) as temp:
        temp.write(b"name: Test")
        temp_name = temp.name

    # Load the yaml file
    result = load_yaml_file2dict(temp_name)

    # Check the result
    assert result == {"name": "Test"}, "Failed to load YAML file to dictionary"

    # Clean up
    os.remove(temp_name)


def test_dump_yaml_file():
    # Create a temporary yaml file
    with tempfile.NamedTemporaryFile(suffix=".yaml", delete=False) as temp:
        temp_name = temp.name

    # Dump data to the yaml file
    dump_yaml_file(temp_name, "name: Test")

    # Load the yaml file
    with open(temp_name, "r") as f:
        result = f.read()

    # Check the result
    assert result == "name: Test\n", "Failed to dump data to YAML file"

    # Clean up
    os.remove(temp_name)


def test_rmdir_if_exists():
    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()

    # Remove the directory
    rmdir_if_exists(temp_dir)

    # Check the directory no longer exists
    assert not os.path.exists(temp_dir), "Failed to remove the directory"


def test_mkdir_if_notexists():
    # Create a temporary directory and remove it
    temp_dir = tempfile.mkdtemp()
    os.rmdir(temp_dir)

    # Create the directory
    mkdir_if_notexists(temp_dir)

    # Check the directory exists
    assert os.path.exists(temp_dir), "Failed to create the directory"

    # Clean up
    os.rmdir(temp_dir)


def test_copy_clobber():
    # Create a source and target directory
    source_dir = tempfile.mkdtemp()
    target_dir = tempfile.mkdtemp()

    # Copy the source to the target
    copy_clobber(source_dir, target_dir)

    # Check the target directory exists
    assert os.path.exists(target_dir), "Failed to copy and clobber the directory"

    # Clean up
    os.rmdir(source_dir)
    os.rmdir(target_dir)


def test_copy_dir():
    # Create a source and target directory
    source_dir = tempfile.mkdtemp()
    target_dir = tempfile.mkdtemp()

    # Copy the source to the target
    copy_dir(source_dir, target_dir)

    # Check the target directory exists
    assert os.path.exists(target_dir), "Failed to copy the directory"

    # Clean up
    os.rmdir(source_dir)
    os.rmdir(target_dir)


def test_copy_file():
    # Create a source and target file
    with tempfile.NamedTemporaryFile(delete=False) as source_file:
        source_file.write(b"Test")
        source_file_name = source_file.name
    with tempfile.NamedTemporaryFile(delete=False) as target_file:
        target_file_name = target_file.name

    # Copy the source to the target
    copy_file(source_file_name, target_file_name)

    # Check the target file exists
    assert os.path.exists(target_file_name), "Failed to copy the file"

    # Clean up
    os.remove(source_file_name)
    os.remove(target_file_name)
