from textwrap import dedent

import pytest

from bashautodoc.function_dependency_processor import FunctionDependencyProcessor
from tests.data_function_dependecy_processor import *


@pytest.mark.parametrize(
    "func_name_list, func_text_dict",
    [
        (
            func_name_list_data1,
            func_text_dict_data1,
        ),
        (
            func_name_list_data2,
            func_text_dict_data2,
        ),
    ],
)
def test_init(func_name_list, func_text_dict):
    processor = FunctionDependencyProcessor(func_name_list, func_text_dict)
    assert (
        processor.func_name_list == func_name_list
    ), "func_name_list not initialized correctly"

    assert (
        processor.func_text_dict == func_text_dict
    ), "func_text_dict not initialized correctly"

    assert processor.func_dep_dict == {}, "func_dep_dict not initialized correctly"


# def test_remove_comment_lines():
#     processor = FunctionDependencyProcessor([], {})
#     cleaned = processor._remove_comment_lines(
#         "# This is a comment\nThis is not a comment"
#     )
#     assert cleaned == "This is not a comment", "Failed to remove comment lines  - test1"


# def test_remove_comment_lines2():
#     processor = FunctionDependencyProcessor([], {})
#     triple_var = """
#     # This is a comment
#     This is not a comment
#     """
#     cleaned = processor._remove_comment_lines(dedent(triple_var))
#     assert cleaned == "This is not a comment", "Failed to remove comment lines - test2"


# @pytest.mark.parametrize(
#     "test_input, expected",
#     [
#         (
#             triple_var2_input,
#             triple_var2_expected,
#         )
#     ],
# )
# def test_remove_comment_lines3(test_input, expected):
#     processor = FunctionDependencyProcessor([], {})

#     cleaned = processor._remove_comment_lines(test_input)
#     assert cleaned == expected, "Failed to remove comment lines - test3"


# @pytest.mark.parametrize(
#     "func_name_list, func_text_dict, func_dep_dict_expected",
#     [
#         (
#             func_name_list_data1,
#             func_text_dict_data1,
#             func_dep_dict_data1_expected,
#         ),
#         (func_name_list_data2, func_text_dict_data2, func_dep_dict_data2_expected),
#     ],
# )
# def test_process_func_def(func_name_list, func_text_dict, func_dep_dict_expected):
#     # func_name_list = ["func1", "func2"]
#     # func_text_dict = {"func1": "def func1(): pass", "func2": "def func2(): pass"}
#     processor = FunctionDependencyProcessor(func_name_list, func_text_dict)

#     for parent_funcname, multiline_fdef in func_text_dict.items():
#         processor._process_func_def(parent_funcname, multiline_fdef)
#         assert (
#             processor.func_dep_dict == func_dep_dict_expected[parent_funcname]
#         ), "Failed to process function definition"


# @pytest.mark.parametrize(
#     "func_name_list, func_text_dict",
#     [
#         (
#             func_name_list_data1,
#             func_text_dict_data1,
#         ),
#         (
#             func_name_list_data2,
#             func_text_dict_data2,
#         ),
#     ],
# )
# def test_isfunc_name_in_multiline_fdef(func_name_list, func_text_dict):
#     processor = FunctionDependencyProcessor(func_name_list, func_text_dict)

#     is_in_def = processor._isfunc_name_in_multiline_fdef(
#         "my_amazing_func", "function func1()\n echo $(my_amazing_func)"
#     )

#     assert is_in_def, "Failed to find function name in multiline function definition"


# def test_isfunc_name_in_multiline_fdef2():
#     processor = FunctionDependencyProcessor([], {})
#     is_in_def = processor._isfunc_name_in_multiline_fdef(
#         "my_amazing_func", "function func1()\n echo 'my_amazing_func '"
#     )
#     assert is_in_def, "Failed to find function name in multiline function definition 2"


# def test_add_funcname_to_dep_dict():
#     processor = FunctionDependencyProcessor([], {})
#     processor._add_funcname_to_dep_dict("parent_func1", "child_func2")
#     assert processor.func_dep_dict == {
#         "parent_func1": ["child_func2"]
#     }, "Failed to add function name to dependency dictionary"


# def test_process_func_def():
#     func_name_list = ["func1", "func2"]
#     func_text_dict = {"func1": "def func1(): pass", "func2": "def func2(): pass"}
#     processor = FunctionDependencyProcessor(func_name_list, func_text_dict)
#     processor._process_func_def("def func1(): func2()", "func1")
#     assert processor.func_dep_dict == {
#         "func1": ["func2"]
#     }, "Failed to process function definition"


# def test_create_func_dep_dict():
#     func_name_list = ["func1", "func2"]
#     func_text_dict = {"func1": "def func1(): func2()", "func2": "def func2(): pass"}
#     processor = FunctionDependencyProcessor(func_name_list, func_text_dict)
#     func_dep_dict = processor.create_func_dep_dict()
#     assert func_dep_dict == {
#         "func1": ["func2"]
#     }, "Failed to create function dependency dictionary"


# # generate tests for selected file using pytest and the following data structures for different test cases:

# # test case1: func_dep_dict = {'colsw': ['_check_integer', '_check_theme_range'], 'colsw_path': ['_check_integer', '_check_theme_range'], 'csp1': ['col_set_prompt_style'], 'csp2': ['col_set_prompt_style'], '_virtualenv_info': ['_virtualenv_min_info']}
# # func_name_list = ['_check_integer', '_check_theme_range', 'colsw', 'colsw_path', 'col_set_prompt_style', 'csp1', 'csp2', 'csp3', 'col_cp_root', 'col_ssh', '_virtualenv_info', '_virtualenv_min_info', '_ssh_info', '_aws_info', '_pwdtail']

# # test case2: func_name_list = [] func_dep_dict = {}

# # test case3: func_dep_dict = {'check_alias_clashes': ['up'], 'mkcd': ['up']} func_name_list = ['check_alias_clashes', 'mkcd', 'up']
# # func_text_dict = {
# #     'check_alias_clashes': 'function check_alias_clashes() {\n\tabout \'Check alias clashes\'\n\tgroup \'aliases\'\n\texample \'$ check_alias_clashes\'\n\n\t# alias lists defined aliases and sed extracts their name.\n\t# The while
# # loop runs type -ta on each of them and awk\n\t# prints the lines that both contain alias and file.\n\talias | sed \'s/^[^ ]* *\\|=.*$//g\' | while read a; do\n\tprintf "%20.20s : %s\\n" $a "$(type -ta $a | tr \'\\n\' \'
# # \')"\n\tdone | awk -F: \'$2 ~ /file/\'\n}\n\n',
# #     'mkcd': 'function mkcd() {\n\tabout \'Make a folder and go into it\'\n\tgroup \'aliases\'\n\tparam \'1: Name of the directory to create & enter\'\n\texample \'mkcd my_new_dir\'\n\n    mkdir -p $1; cd $1\n}\n\n\n# ls
# # commands\n\n# switch to use exa instead of ls if available on system\nif command -v exa >/dev/null; then\n    alias ls=\'${HOME}/stablecaps_bashrc/internal/internal_exa_wrapper.sh\'\nelse\n    alias ls=\'/bin/ls -ah
# # --color=always\'\nfi\n\n#alias ls=\'ls -ah --color=always\' # ls always has --color switched on & shows all files\n\n# exa - uncomment if it is installed on the system\n# https://github.com/sharkdp/vivid # to generate LS_COLORS\n#
# # https://github.com/trapd00r/LS_COLORS\n#ayu\n\n\n# function exlt() {\n# \tabout \'Exa long with tree view with option to limit the number of levels\'\n# \tgroup \'aliases\'\n# \tparam \'number of levels\'\n# \texample \'$ exlt\'\n#
# # \texample \'$ exlt 2\'\n\n# \tlocal num_levels=$1\n# \tif [ num_levels == "" ]; then\n# \t\texa -al --group --links --grid --tree --color=automatic --classify --level\n# \telse\n# \t\texa -al --group --links --grid --tree
# # --color=automatic --classify --level $num_levels\n# \tfi\n# }\n\n# exa --ignore-glob="*case*"\n# exa --ignore-glob="Open*|rot??.sh|*case*"\n# exa --sort=ext\n\n\n\n# cd commands\n\n# Goes up a specified number of directories  (i.e.
# # up 4)',
# #     'up': 'function up() {\n\tabout \'Go up N directories in the file path\'\n\tgroup \'aliases\'\n\tparam \'1: Integer corresponding to number of directories to go up.\'\n\texample \'$ up 3\'\n\n\tlocal d=""\n\tlimit=$1\n\tfor
# # ((i=1 ; i <= limit ; i++))\n\t\tdo\n\t\t\td=$d/..\n\t\tdone\n\td=$(echo $d | sed \'s/^\\///\')\n\tif [ -z "$d" ]; then\n\t\td=..\n\tfi\n\tcd $d\n}\n\n# other commands\n\n\n\n## df -\n\n\n### bat\n\nhelp() {\n\tabout \'Uses bat to
# # colorize help text messages\'\n\tgroup \'aliases\'\n\tparam \'Name of program whose help text we wish to pipe to bat\'\n\texample \'$ help mv\'\n\texample \'$ help git commit\'\n    "$@" --help 2>&1 | bathelp\n}'
# # }
