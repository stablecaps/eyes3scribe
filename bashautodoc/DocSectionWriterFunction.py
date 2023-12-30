import logging

from bashautodoc.function_call_tree import draw_tree, parser
from bashautodoc.helpo.hstrops import rm_lines_starting_with

LOG = logging.getLogger(__name__)


class DocSectionWriterFunction:
    def __init__(self, mdFile, func_text_dict, func_dep_dict, cite_parameters):
        self.mdFile = mdFile
        self.func_text_dict = func_text_dict
        self.sh2_md_file_writers = cite_parameters
        self.func_dep_dict = func_dep_dict

    def _write_function_index(self):
        """
        Write the function index to the markdown file.

        Example:
            writer._write_function_index()
        """
        self.mdFile.new_header(
            level=2, title="Function Index", style="atx", add_table_of_contents="n"
        )
        func_index_li = [
            str(idx + 1).rjust(2, "0") + " - " + key
            for idx, key in enumerate(self.func_text_dict.keys())
        ]
        cat_all_funcs = "\n".join(func_index_li)
        self.mdFile.insert_code(cat_all_funcs, language="python")

    def _write_page_header(self, func_name):
        """
        Write the page header to the markdown file.

        Args:
            func_name (str): The name of the function.

        Example:
            writer._write_page_header('my_function')
        """
        self.mdFile.new_paragraph("******")
        self.mdFile.new_header(
            level=3, title=f">> {func_name}():", style="atx", add_table_of_contents="n"
        )

    def _gen_cite_parameter_strings(self, func_str):
        """
        Generate citation parameter strings.

        Args:
            func_str (str): The function string.

        Returns:
            list: A list of citation parameter strings.

        Example:
            citation_strings = writer._gen_cite_parameter_strings('my_function')
        """
        cite_li = []
        for line in func_str.split("\n"):
            print("line", line)
            for cparam in self.sh2_md_file_writers:
                max_str_prefix_len = 11
                if cparam in line.strip()[0:max_str_prefix_len]:
                    stripped_line = line.strip().replace(f"{cparam} '", f"{cparam} ")
                    LOG.debug(
                        "*!! %s, %s, %s, %s",
                        line.strip()[0:max_str_prefix_len],
                        "8",
                        cparam,
                        stripped_line,
                    )

                    cparam_replacement = ">***" + cparam.strip("'").strip() + "***: "
                    stripped_line_fmt = (
                        stripped_line.strip("'")
                        .strip()
                        .replace(cparam, cparam_replacement)
                        + "\n"
                    )
                    if cparam == "example '":
                        ### Put example in inline code block
                        LOG.debug("stripped_line_fmt0: %s", stripped_line_fmt)

                        example_fmt = stripped_line_fmt.replace("***: ", """***: `""")
                        stripped_line_fmt = example_fmt[:-1] + "`\n"
                        LOG.debug("stripped_line_fmt1: %s", stripped_line_fmt)

                    LOG.debug("stripped_line_fmt: %s", stripped_line_fmt)
                    cite_li.append(stripped_line_fmt)
        LOG.debug("cite_li: %s", cite_li)
        return cite_li

    def _add_about_param_example_etc(self, func_str):
        """
        Add information about parameters and examples to the markdown file.

        Args:
            func_str (str): The function string.

        Example:
            writer._add_about_param_example_etc('my_function')
        """
        cite_li = self._gen_cite_parameter_strings(func_str=func_str)
        # if cite_li is not None:
        if len(cite_li) > 0:
            LOG.debug("cite_li %s", cite_li)
            # sys.exit(42)
            for cparam_str in cite_li:
                self.mdFile.new_paragraph(cparam_str)

    def clean_func_str(self, multiline_str):
        """
        Clean a multiline string by removing lines starting with certain patterns.

        Args:
            multiline_str (str): The multiline string to clean.

        Returns:
            str: The cleaned string.

        Example:
            cleaned_str = writer.clean_func_str('my_multiline_string')
        """
        full_cleaned = rm_lines_starting_with(
            multiline_str=multiline_str,
            rm_patt_list=["#", "about", "example", "group", "param"],
        ).rstrip("\n")

        return full_cleaned

    def _add_function_code_block(self, func_str):
        """
        Add a code block to the markdown file containing function src code.

        Args:
            func_str (str): The function string.

        Example:
            writer._add_function_code_block('my_function')
        """
        cleaned_func_str = self.clean_func_str(multiline_str=func_str)
        LOG.debug("cleaned_func_str %s", cleaned_func_str)

        self.mdFile.insert_code(code=cleaned_func_str, language="bash")

    def gen_func_dependent_str(self, func_name):
        """
        Generate a string representing the dependencies of a function.

        Args:
            func_name (str): The name of the function.

        Returns:
            str: A string representing the dependencies of the function.

        Example:
            dependencies = writer.gen_func_dependent_str('my_function')
        """
        func_name = func_name.strip("()")

        called_funcs = self.func_dep_dict.get(func_name, None)

        LOG.debug("self.func_dep_dict %s", self.func_dep_dict)
        LOG.debug("called_funcs %s %s", func_name, called_funcs)

        if called_funcs is None:
            return None

        called_funcs_str = " ".join(called_funcs)
        stringify_funccalls = f"{func_name}: {called_funcs_str}\n"

        for cfunc in called_funcs:
            if cfunc in self.func_dep_dict:
                # make a dependent string
                dependent_func = " ".join(self.func_dep_dict[cfunc])
                stringify_funccalls += f"{cfunc}: {dependent_func}\n"
        LOG.debug("stringify_funccalls %s", stringify_funccalls)

        return stringify_funccalls

    def _add_function_dependency_block(self, func_name):
        """
        Add a block to the markdown file representing the dependencies of a function.

        Args:
            func_name (str): The name of the function.

        Example:
            writer._add_function_dependency_block('my_function')
        """
        multiline_funccalls_input = self.gen_func_dependent_str(func_name=func_name)
        multiline_funccalls_output = None
        LOG.debug("multiline_funccalls_input %s", multiline_funccalls_input)

        if multiline_funccalls_input is not None:
            multiline_funccalls_output = draw_tree(parser(multiline_funccalls_input))
        LOG.debug(
            "\nmultiline_funccalls_output\n %s %s",
            multiline_funccalls_output,
            type(multiline_funccalls_output),
        )

        if multiline_funccalls_output is not None:
            self.mdFile.new_header(
                level=5, title="Function Calls:", style="atx", add_table_of_contents="n"
            )
            self.mdFile.insert_code(code=multiline_funccalls_output, language="bash")
        self.mdFile.new_paragraph("\n")

    def _generate_markdown_code_from_function_signature(self):
        """
        Generate markdown sections with parameter and example documentation for each function in the function text dictionary.

        Example:
            writer._generate_markdown_code_from_function_signature()
        """
        for func_name, func_str in self.func_text_dict.items():
            LOG.debug("\n*~~~~~\n %s", func_name)  # , "\n", func_str)
            self._write_page_header(func_name)
            self._add_about_param_example_etc(func_str)
            self._add_function_code_block(func_str)
            self._add_function_dependency_block(func_name)

    def write_func_section(self):
        """
        Entrypoint that writes the function section to the markdown file.

        Example:
            writer.write_func_section()
        """
        self._write_function_index()
        self._generate_markdown_code_from_function_signature()
