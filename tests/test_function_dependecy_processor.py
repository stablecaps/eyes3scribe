import pytest
from autodocumatix.function_dependency_processor import FunctionDependencyProcessor


@pytest.fixture
def setup_function():
    func_name_list = [
        "_check_integer",
        "_check_theme_range",
        "colsw",
        "colsw_path",
        "col_set_prompt_style",
        "csp1",
        "csp2",
        "csp3",
        "col_cp_root",
        "col_ssh",
        "_virtualenv_info",
        "_virtualenv_min_info",
        "_ssh_info",
        "_aws_info",
        "_pwdtail",
    ]
    func_text_dict = {}  # You need to provide function definitions here
    processor = FunctionDependencyProcessor(func_name_list, func_text_dict)
    return processor


def test_create_func_dep_dict_case1(setup_function):
    expected = {
        "colsw": ["_check_integer", "_check_theme_range"],
        "colsw_path": ["_check_integer", "_check_theme_range"],
        "csp1": ["col_set_prompt_style"],
        "csp2": ["col_set_prompt_style"],
        "_virtualenv_info": ["_virtualenv_min_info"],
    }
    result = setup_function.create_func_dep_dict()
    assert (
        result == expected
    ), "Failed to create function dependency dictionary for case 1"


def test_create_func_dep_dict_case2(setup_function):
    setup_function.func_name_list = []
    expected = {}
    result = setup_function.create_func_dep_dict()
    assert (
        result == expected
    ), "Failed to create function dependency dictionary for case 2"


def test_create_func_dep_dict_case3(setup_function):
    setup_function.func_name_list = ["check_alias_clashes", "mkcd", "up"]
    expected = {"check_alias_clashes": ["up"], "mkcd": ["up"]}
    result = setup_function.create_func_dep_dict()
    assert (
        result == expected
    ), "Failed to create function dependency dictionary for case 3"


# generate tests for selected file using pytest and the following data structures for different test cases:

# test case1: func_dep_dict = {'colsw': ['_check_integer', '_check_theme_range'], 'colsw_path': ['_check_integer', '_check_theme_range'], 'csp1': ['col_set_prompt_style'], 'csp2': ['col_set_prompt_style'], '_virtualenv_info': ['_virtualenv_min_info']}
# func_name_list = ['_check_integer', '_check_theme_range', 'colsw', 'colsw_path', 'col_set_prompt_style', 'csp1', 'csp2', 'csp3', 'col_cp_root', 'col_ssh', '_virtualenv_info', '_virtualenv_min_info', '_ssh_info', '_aws_info', '_pwdtail']

# test case2: func_name_list = [] func_dep_dict = {}

# test case3: func_dep_dict = {'check_alias_clashes': ['up'], 'mkcd': ['up']} func_name_list = ['check_alias_clashes', 'mkcd', 'up']
