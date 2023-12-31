import logging

from rich import print as print

from bashautodoc.helpo.hstrops import rm_lines_starting_with

LOG = logging.getLogger(__name__)


class FunctionDependencyProcessor:
    """
    Processes function dependencies.

    Attributes:
        func_name_list (list): List of function names.
        func_text_dict (dict): Dictionary of function texts.
        func_dep_dict (dict): Dictionary of function dependencies.

    Example:
        processor = FunctionDependencyProcessor(func_name_list, func_text_dict)
        func_dep_dict = processor.gen_func_dep_dict()
    """

    def __init__(self, func_name_list, func_text_dict):
        """
        Initializes the FunctionDependencyProcessor.

        Args:
            func_name_list (list): List of function names.
            func_text_dict (dict): Dictionary of function texts.
        """
        self.func_name_list = func_name_list
        self.func_text_dict = func_text_dict

        self.func_dep_dict = {}

    def _isfunc_name_in_multiline_fdef(self, func_name, clean_parent_multiline_fdef):
        """
        Checks if a function name is in a multiline function definition.

        Args:
            func_name (str): The function name.
            clean_parent_multiline_fdef (str): The clean multiline function definition.

        Returns:
            bool: True if the function name is in the definition, False otherwise.

        Example:
            is_in_def = self._isfunc_name_in_multiline_fdef(func_name, clean_parent_multiline_fdef)
        """
        func_name_with_space = f"{func_name} "
        func_name_with_dollar = f"$({func_name})"
        return (func_name_with_space in clean_parent_multiline_fdef) or (
            func_name_with_dollar in clean_parent_multiline_fdef
        )

    def _add_funcname_to_dep_dict(self, parent_funcname, child_funcname):
        """
        Adds a function name to the dependency dictionary.

        Args:
            parent_funcname (str): The parent function name.
            child_funcname (str): The child function name.

        Example:
            self._add_funcname_to_dep_dict(parent_funcname, child_funcname)
        """
        if parent_funcname not in self.func_dep_dict:
            # create new entry
            self.func_dep_dict[parent_funcname] = [child_funcname]
        else:
            # append to existing list
            if child_funcname not in self.func_dep_dict[parent_funcname]:
                # check for existing value in list
                self.func_dep_dict[parent_funcname].append(child_funcname)

    def _process_func_def(self, clean_parent_multiline_fdef, parent_funcname):
        """
        Processes a function definition.

        Args:
            clean_parent_multiline_fdef (str): The clean multiline function definition.
            parent_funcname (str): The parent function name.

        Example:
            self._process_func_def(clean_parent_multiline_fdef, parent_funcname)
        """
        for child_funcname in self.func_name_list:
            # exclude functions own name
            if (
                child_funcname != parent_funcname
                and self._isfunc_name_in_multiline_fdef(
                    child_funcname, clean_parent_multiline_fdef
                )
            ):
                self._add_funcname_to_dep_dict(parent_funcname, child_funcname)

    def gen_func_dep_dict(self):
        """
        Creates a function dependency dictionary.

        Returns:
            dict: The function dependency dictionary.

        Example:
            func_dep_dict = self.gen_func_dep_dict()
        """
        LOG.debug("func_name_list = %s", self.func_name_list)
        LOG.debug("func_text_dict = %s", self.func_text_dict)

        for parent_funcname, multiline_fdef in self.func_text_dict.items():
            clean_parent_multiline_fdef = rm_lines_starting_with(
                multiline_str=multiline_fdef, rm_patt_list=["#"]
            )

            print("clean_parent_multiline_fdef", clean_parent_multiline_fdef)

            self._process_func_def(
                clean_parent_multiline_fdef=clean_parent_multiline_fdef,
                parent_funcname=parent_funcname,
            )

        # if len(self.func_name_list) > 4:
        #     print("parent_funcname", parent_funcname)
        #     print("multiline_fdef", multiline_fdef)

        #     print("self.func_dep_dict", self.func_dep_dict)
        #     import sys

        #     sys.exit(42)
        return self.func_dep_dict
