import logging

from rich import print as print

from autodocumatix.helpo.hstrops import rm_lines_starting_with

LOG = logging.getLogger(__name__)


class FunctionDependencyProcessor:
    def __init__(self, func_name_list, func_text_dict):
        self.func_name_list = func_name_list
        self.func_text_dict = func_text_dict

        self.func_dep_dict = {}

    def _remove_comment_lines(self, multiline_str):
        return rm_lines_starting_with(multiline_str=multiline_str, rm_patt_list=["#"])

    def _func_name_in_def(self, func_name, cleaned_ml_fdef):
        return (func_name + " " in cleaned_ml_fdef) or (
            "(" + func_name + ")" in cleaned_ml_fdef
        )

    def _add_func_to_dep_dict(self, func_name, key):
        if key not in self.func_dep_dict:
            # create new entry
            self.func_dep_dict[key] = [func_name]
        else:
            # append to existing list
            if func_name not in self.func_dep_dict[key]:  # unique values
                self.func_dep_dict[key].append(func_name)

    def _process_func_def(self, cleaned_ml_fdef, func_name_list, key):
        for func_name in func_name_list:
            # exclude functions own name
            if func_name != key and self._func_name_in_def(func_name, cleaned_ml_fdef):
                self._add_func_to_dep_dict(func_name, key)

    def create_func_dep_dict(self):
        LOG.debug("func_name_list = %s", self.func_name_list)

        for key, multiline_fdef in self.func_text_dict.items():
            cleaned_ml_fdef = self._remove_comment_lines(multiline_fdef)
            self._process_func_def(cleaned_ml_fdef, self.func_name_list, key)

        return self.func_dep_dict
