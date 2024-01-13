import logging
from dataclasses import dataclass

from eyes3scribe.function_dependency_processor import FunctionDependencyProcessor
from eyes3scribe.helpo.hstrops import str_multi_replace

LOG = logging.getLogger(__name__)


# TODO: enable slots=True
# @dataclass(slots=True)
@dataclass()
class FunctionDataHolder:
    srcfile_rpath: str = None
    #
    func_name_list: list[str] = None
    full_alias_str_list: list[str] = None
    cite_about: str = None
    func_text_dict: dict[str, str] = None
    func_dep_dict: dict[str, list[str]] = None


class FunctionDatahandler:
    def __new__(cls, srcfile_rpath: str):
        # https://stackoverflow.com/questions/2491819/how-to-return-a-value-from-init-in-python
        cls.funcdata = FunctionDataHolder()
        cls.funcdata.srcfile_rpath = srcfile_rpath

        return cls.main()

    @staticmethod
    def _get_function_name(line_str):
        """
        Extracts the function name from a line of shell script.

        Args:
            line_str (str): A line of shell script.

        Returns:
            str: The name of the function.

        Example:
            function_name = ShellSrcPreProcessor._get_function_name("function hello_world {")
        """
        func_name = None
        if line_str.strip().endswith(("{", "}")):
            function_header = line_str.split()
            func_name = function_header[1].strip("()")
            LOG.debug("func_name: %s", func_name)
        return func_name

    @staticmethod
    def _process_alias_line(line):
        """
        Process a line of code containing an alias definition.

        Args:
            line (str): Line of code.

        Returns:
            str: Processed alias string.

        Example:
            preprocessor = ShellSrcPreProcessor(cnf="config",
                                                clean_srcfiles_rpaths=["file1", "file2"],
                                                project_docs_dir="docs/",
                                                debug=True)
            alias_string = preprocessor._process_alias_line("alias ls='ls -l' # List files")
        """
        LOG.debug("line: %s", line)

        alias_list = line.replace("alias ", "").strip().split("=", 1)
        LOG.debug("alias_list: %s", alias_list)

        if len(alias_list) < 2:
            return None

        alias_name = alias_list[0]
        alias_cmd = alias_list[1]
        alias_comment = ""

        if "#" in alias_list[1]:
            alias_list_lvl2 = alias_list[1].split("#", 1)
            alias_cmd = alias_list_lvl2[0]
            alias_comment = alias_list_lvl2[1]

        return f"| **{alias_name}** | `{alias_cmd[1:-1]}` | {alias_comment}\n"

    @classmethod
    def _gen_func_text_dict(cls):
        """
        Create a dictionary of function names and their corresponding code.

        Args:
            srcfile_rpath (str): Path to the src file.

        Returns:
            tuple: Tuple containing function name list, alias string list,
                   about citation, and function text dictionary.

        Example:
            preprocessor = ShellSrcPreProcessor(cnf="config",
                                                clean_srcfiles_rpaths=["file1", "file2"],
                                                project_docs_dir="docs/",
                                                debug=True)
            func_name_list, alias_str_list, cite_about, func_text_dict =
                preprocessor._gen_func_text_dict("file1")
        """
        func_name_list = []
        full_alias_str_list = []
        func_name = None
        cite_about = "Undefined. Add composure cite-about to shell script file"

        with open(cls.funcdata.srcfile_rpath, "r") as FHI:
            LOG.debug("cls.funcdata.srcfile_rpath: %s", cls.funcdata.srcfile_rpath)

            func_text_dict = {}
            src_text = FHI.read()

            for line in src_text.split("\n"):
                if line.startswith("function"):
                    func_name = FunctionDatahandler._get_function_name(line)
                    if func_name:
                        func_name_list.append(func_name)
                        func_text_dict[func_name] = line
                # TODO: remove hardcoded "about" strings
                elif line.startswith(
                    (
                        "about-plugin",
                        "about-alias",
                        "about-completion",
                        "about-module",
                        "about-internal",
                    )
                ):
                    cite_about = str_multi_replace(
                        instr=line,
                        rm_patt_list=[
                            "about-plugin",
                            "about-alias",
                            "about-completion",
                            "about-module",
                            "about-internal",
                            "'",
                        ],
                        replace_str="",
                    ).strip()
                elif line.startswith("alias"):
                    alias_str = FunctionDatahandler._process_alias_line(line)
                    if alias_str:
                        full_alias_str_list.append(alias_str)
                else:
                    if func_name:
                        func_text_dict[func_name] += "\n" + line

        cls.funcdata.func_name_list = func_name_list
        cls.funcdata.full_alias_str_list = full_alias_str_list
        cls.funcdata.cite_about = cite_about
        cls.funcdata.func_text_dict = func_text_dict
        # return func_name_list, full_alias_str_list, cite_about, func_text_dict

    @classmethod
    def main(cls):
        cls._gen_func_text_dict()

        func_dep_processor = FunctionDependencyProcessor(
            func_name_list=cls.funcdata.func_name_list,
            func_text_dict=cls.funcdata.func_text_dict,
        )
        cls.funcdata.func_dep_dict = func_dep_processor.gen_func_dep_dict()

        return cls.funcdata
