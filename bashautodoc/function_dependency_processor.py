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
        func_dep_dict = processor.create_func_dep_dict()
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

    def _remove_comment_lines(self, multiline_str):
        """
        Removes comment lines from a multiline string.

        Args:
            multiline_str (str): The multiline string.

        Returns:
            str: The cleaned multiline string.

        Example:
            cleaned = self._remove_comment_lines(multiline_str)
        """
        return rm_lines_starting_with(multiline_str=multiline_str, rm_patt_list=["#"])

    def _isfunc_name_in_multiline_fdef(self, func_name, cleaned_parent_multiline_fdef):
        """
        Checks if a function name is in a multiline function definition.

        Args:
            func_name (str): The function name.
            cleaned_parent_multiline_fdef (str): The cleaned multiline function definition.

        Returns:
            bool: True if the function name is in the definition, False otherwise.

        Example:
            is_in_def = self._isfunc_name_in_multiline_fdef(func_name, cleaned_parent_multiline_fdef)
        """
        func_name_with_space = f"{func_name} "
        func_name_with_dollar = f"$({func_name})"
        return (func_name_with_space in cleaned_parent_multiline_fdef) or (
            func_name_with_dollar in cleaned_parent_multiline_fdef
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

    def _process_func_def(self, cleaned_parent_multiline_fdef, parent_funcname):
        """
        Processes a function definition.

        Args:
            cleaned_parent_multiline_fdef (str): The cleaned multiline function definition.
            parent_funcname (str): The parent function name.

        Example:
            self._process_func_def(cleaned_parent_multiline_fdef, parent_funcname)
        """
        for child_funcname in self.func_name_list:
            # exclude functions own name
            if (
                child_funcname != parent_funcname
                and self._isfunc_name_in_multiline_fdef(
                    child_funcname, cleaned_parent_multiline_fdef
                )
            ):
                self._add_funcname_to_dep_dict(parent_funcname, child_funcname)

    def create_func_dep_dict(self):
        """
        Creates a function dependency dictionary.

        Returns:
            dict: The function dependency dictionary.

        Example:
            func_dep_dict = self.create_func_dep_dict()
        """
        LOG.debug("func_name_list = %s", self.func_name_list)

        for parent_funcname, multiline_fdef in self.func_text_dict.items():
            cleaned_parent_multiline_fdef = self._remove_comment_lines(multiline_fdef)

            self._process_func_def(
                cleaned_parent_multiline_fdef=cleaned_parent_multiline_fdef,
                parent_funcname=parent_funcname,
            )

        return self.func_dep_dict
