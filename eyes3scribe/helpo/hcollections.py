import logging
from collections import Mapping

LOG = logging.getLogger(__name__)

####################################################################
### Lists
###


def clean_list_via_rm_patts(input_list, rm_patts, rm_empty_instrs=True):
    """
    Cleans a list by removing elements that are empty or contain any of the specified patterns.

    Args:
        input_list (list): The list to be cleaned.
        rm_patts (list): The patterns to remove.
        rm_empty_instrs (bool, optional): Whether to remove empty strings. Defaults to True.

    Returns:
        list: The cleaned list.

    Example:
        >>> clean_list_via_rm_patts(["Hello", "World", "", "Hello, World"], ["World"])
        ['Hello', '']
    """
    clean_list = []
    for instr in input_list:
        instr_is_empty = len(instr.strip()) == 0
        instr_contains_rm_patts = any(rm_patt in instr for rm_patt in rm_patts)

        if instr_is_empty and rm_empty_instrs:
            continue
        if instr_contains_rm_patts:
            continue

        clean_list.append(instr)
    return clean_list


####################################################################
### Dictionaries
###


def find_nested_key(my_json, find_key):
    """Search in a nested dict for a key or None."""
    if find_key in my_json:
        return my_json[find_key]

    for _, vval in my_json.items():
        if isinstance(vval, dict):
            item = find_nested_key(vval, find_key)
            if item is not None:
                return item
    return None


def nested_dic_update(base_dic, in_dic):
    """Recursively merge two nested dictionaries together."""
    for kkey, vval in in_dic.items():
        if isinstance(vval, Mapping):
            recursive_call = nested_dic_update(base_dic.get(kkey, {}), vval)
            base_dic[kkey] = recursive_call
        else:
            base_dic[kkey] = in_dic[kkey]
    return base_dic


def find_replace_dict_values(mydict, search_key, old_value, new_value):
    "Recursively find and replace values in a nested dict"
    for key, val in mydict.items():
        if key == search_key:
            if val == old_value:
                mydict[key] = new_value
        elif isinstance(mydict[key], dict):
            find_replace_dict_values(mydict[key], search_key, old_value, new_value)
    return mydict


def stringify_dict_2list(inlist):
    """
    Converts a list of values into a list of strings.

    Args:
        inlist (list): The input list of values.

    Returns:
        list: A list of strings representing the values.

    Raises:
        Exception: If an item in the input list cannot be converted to a string.

    Examples:
        >>> stringify_values([1, 2, 3])
        ['1', '2', '3']

        >>> stringify_values(['a', 'b', 'c'])
        ['a', 'b', 'c']

        >>> stringify_values([{'key1': 'value1', 'key2': 'value2'}, {'key3': 'value3'}])
        ['key1 value1, key2 value2,', 'key3 value3,']

        >>> stringify_values([1, 'a', {'key': 'value'}])
        ['1', 'a', 'key value,']
    """
    string_items = []
    for item in inlist:
        if isinstance(item, dict):
            new_item = " ".join(f"{key} {val}" for key, val in item.items())
            string_items.append(new_item)
        elif isinstance(item, int):
            new_item = str(item)
            string_items.append(new_item)
        elif isinstance(item, str):
            string_items.append(item)
        else:
            LOG.error("failed stringify item is %s, type: %s", item, type(item))
            raise Exception("failed stringify item is ", item, type(item))
    return string_items


def flatten_list(nested_list):
    # TODO: move into collection helpers
    flat_list = []
    for sublist in nested_list:
        flat_list.extend(sublist)
    return flat_list
