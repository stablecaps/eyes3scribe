# import os
# import tempfile

# from ruamel.yaml import YAML

# yaml = YAML(typ="safe")

# from eyes3scribe.helpo.hfile import (
#     copy_clobber,
#     copy_dir,
#     copy_file,
#     dump_yaml_file,
#     load_yaml_file2dotmap,
#     mkdir_if_notexists,
#     rmdir_if_exists,
#     write_dict_2yaml_file,
# )


# def test_load_yaml_file2dotmap():
#     # Create a temporary yaml file
#     with tempfile.NamedTemporaryFile(suffix=".yaml", delete=False) as temp:
#         temp.write(b"name: Test")
#         temp_name = temp.name

#     # Load the yaml file
#     result = load_yaml_file2dotmap(temp_name)

#     # Check the result
#     assert result == {
#         "name": "Test"
#     }, "The loaded YAML data does not match the expected result"

# # Clean up
# os.remove(temp_name)


# def test_dump_yaml_file():
#     # Create a temporary yaml file
#     with tempfile.NamedTemporaryFile(suffix=".yaml", delete=False) as temp:
#         temp_name = temp.name

#     # Dump data to the yaml file
#     yaml_string = '"name": "Test"'
#     dump_yaml_file(temp_name, yaml_string)

#     # Load the yaml file
#     with open(temp_name, "r") as f:
#         result = yaml.load(f)

#     # Check the result
#     expected_result = {"name": "Test"}
#     assert result == expected_result, f"Expected {expected_result}, but got {result}"

#     # Clean up
#     os.remove(temp_name)


# def test_write_dict_2yaml_file():
#     # Create a temporary yaml file
#     with tempfile.NamedTemporaryFile(suffix=".yaml", delete=False) as temp:
#         temp_name = temp.name

#     # Write a dictionary to the yaml file
#     yaml_dict = {"name": "Test"}
#     write_dict_2yaml_file(temp_name, yaml_dict)

#     # Load the yaml file
#     with open(temp_name, "r") as f:
#         result = yaml.load(f)

#     # Check the result
#     expected_result = {"name": "Test"}
#     assert result == expected_result, f"Expected {expected_result}, but got {result}"

#     # Clean up
#     os.remove(temp_name)


# def test_rmdir_if_exists():
#     # Create a temporary directory
#     temp_dir = tempfile.mkdtemp()

#     # Remove the directory
#     rmdir_if_exists(temp_dir)

#     # Check the directory no longer exists
#     assert not os.path.exists(temp_dir), "Failed to remove the directory"


# def test_mkdir_if_notexists():
#     # Create a temporary directory and remove it
#     temp_dir = tempfile.mkdtemp()
#     os.rmdir(temp_dir)

#     # Create the directory
#     mkdir_if_notexists(temp_dir)

#     # Check the directory exists
#     assert os.path.exists(temp_dir), "Failed to create the directory"

#     # Clean up
#     os.rmdir(temp_dir)


# def test_copy_clobber():
#     # Create a source and target directory
#     source_dir = tempfile.mkdtemp()
#     target_dir = tempfile.mkdtemp()

#     # Copy the source to the target
#     copy_clobber(source_dir, target_dir)

#     # Check the target directory exists
#     assert os.path.exists(target_dir), "Failed to copy and clobber the directory"

#     # Clean up
#     os.rmdir(source_dir)
#     os.rmdir(target_dir)


# def test_copy_dir():
#     # Create a source and target directory
#     source_dir = tempfile.mkdtemp()
#     target_dir = tempfile.mkdtemp()

#     # Copy the source to the target
#     copy_dir(source_dir, target_dir)

#     # Check the target directory exists
#     assert os.path.exists(target_dir), "Failed to copy the directory"

#     # Clean up
#     os.rmdir(source_dir)
#     os.rmdir(target_dir)


# def test_copy_file():
#     # Create a source and target file
#     with tempfile.NamedTemporaryFile(delete=False) as source_file:
#         source_file.write(b"Test")
#         source_filename = source_file.name
#     with tempfile.NamedTemporaryFile(delete=False) as target_file:
#         target_filename = target_file.name

#     # Copy the source to the target
#     copy_file(source_filename, target_filename)

#     # Check the target file exists
#     assert os.path.exists(target_filename), "Failed to copy the file"

#     # Clean up
#     os.remove(source_filename)
#     os.remove(target_filename)
