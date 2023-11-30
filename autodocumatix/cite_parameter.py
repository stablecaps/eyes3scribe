"""Class to extract composure cite parameters from function src code."""

import sys
import logging
from mdutils.mdutils import MdUtils
from autodocumatix.helpo.hfile import mkdir_if_notexists
from autodocumatix.helpo.hstrops import (
    filter_false_if_str_in_pattern,
    rm_line_containing,
)
from autodocumatix.function_call_tree import draw_tree, parser

LOG = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, stream=sys.stdout)


class CiteParameters:
    def __init__(
        self,
        cite_about,
        func_text_dict,
        func_dep_dict,
        full_alias_str_list,
        src_file_path,
        out_dir,
    ):
        self.cite_about = cite_about
        self.func_text_dict = func_text_dict
        self.func_dep_dict = func_dep_dict
        # print("nnn", func_dep_dict)
        # sys.exit(0)
        self.full_alias_str_list = full_alias_str_list
        self.src_file_path = src_file_path
        self.out_dir = out_dir

        self.cite_parameters = [
            "about '",
            "group '",
            "param '",
            "example '",
        ]  # , "about '", "about '"]

        # self.cparam_sort_mapper = {
        #     ">***about***": 0,
        #     ">***group***": 1,
        #     ">***param***": 2,
        #     ">***example***": 3,
        # }

        self.main_write_md()

    def gen_cite_parameter_strings(self, func_str):
        cite_li = []
        for line in func_str.split("\n"):
            for cparam in self.cite_parameters:
                max_str_prefix_len = 11
                if cparam in line.strip()[0:max_str_prefix_len]:
                    stripped_line = line.strip()
                    # print(
                    #     "*!!",
                    #     line.strip()[0:max_str_prefix_len],
                    #     "8",
                    #     cparam,
                    #     stripped_line,
                    # )

                    cparam_replacement = ">***" + cparam.strip("'").strip() + "***: "
                    stripped_line_fmt = (
                        stripped_line.strip("'")
                        .strip()
                        .replace(cparam, cparam_replacement)
                        + "\n"
                    )
                    if cparam == "example '":
                        ### Put example in inline code block
                        # print("\n\n\nYOOOOOOOO")
                        # print("stripped_line_fmt0", stripped_line_fmt)
                        example_fmt = stripped_line_fmt.replace("***: ", """***: `""")
                        stripped_line_fmt = example_fmt[:-1] + "`\n"
                        # print("stripped_line_fmt1", stripped_line_fmt)
                        # sys, exit(0)

                    print("stripped_line_fmt", stripped_line_fmt)
                    cite_li.append(stripped_line_fmt)
        print("cite_li", cite_li)
        return cite_li  # .sort(key=lambda val: self.cparam_sort_mapper[val[1]])

    # def rm_line_containing(self, multiline_str, rm_patt):
    #     out_str = ""
    #     for line in multiline_str.split("\n"):
    #         if line.strip().startswith(rm_patt):
    #             pass
    #         else:
    #             out_str += line + "\n"
    #     return out_str

    def clean_func_str(self, multiline_str):
        print("multiline_str", multiline_str)
        clean0 = rm_line_containing(multiline_str=multiline_str.strip(), rm_patt="#")

        # TODO: Make this function method chainable
        print("\nclean0\n", clean0)
        clean1 = rm_line_containing(multiline_str=clean0.strip(), rm_patt="about")
        print("\nclean1\n", clean1)
        clean2 = rm_line_containing(multiline_str=clean1.strip(), rm_patt="example")
        print("\nclean2\n", clean2)
        clean3 = rm_line_containing(multiline_str=clean2.strip(), rm_patt="group")
        print("\nclean3\n", clean3)
        clean4 = rm_line_containing(multiline_str=clean3.strip(), rm_patt="param")
        print("\nclean4\n", clean4)

        full_cleaned = clean4
        return full_cleaned

    def gen_func_dependent_str(self, func_name):
        func_name = func_name.strip("()")
        print("nnn", self.func_dep_dict)
        called_funcs = self.func_dep_dict.get(func_name, None)
        print("called_funcs", func_name, called_funcs)

        if called_funcs is None:
            return None
        # else:
        #     print("hooley", called_funcs)
        #     sys.exit(42)

        stringify_funccalls = func_name + ": " + " ".join(called_funcs) + "\n"

        for cfunc in called_funcs:
            if cfunc in self.func_dep_dict:
                # make a dependent string
                stringify_funccalls += (
                    cfunc + ": " + " ".join(self.func_dep_dict[cfunc]) + "\n"
                )
        print(f"\n yo {stringify_funccalls}")
        return stringify_funccalls

    def write_func_section(
        self,
    ):
        ### Function Index
        self.mdFile.new_header(
            level=2, title="Function Index", style="atx", add_table_of_contents="n"
        )

        func_index_li = [
            str(idx + 1).rjust(2, "0") + " - " + key
            for idx, key in enumerate(self.func_text_dict.keys())
        ]
        cat_all_funcs = "\n".join(func_index_li)
        self.mdFile.insert_code(
            cat_all_funcs,
            language="python",
        )

        ### Add composure about, group, param, example settings
        for func_name, func_str in self.func_text_dict.items():
            # print("\n*~~~~~\n", func_name)  # , "\n", func_str)

            ### Page header
            self.mdFile.new_paragraph("******")
            self.mdFile.new_header(
                level=3,
                title=f">> {func_name}():",
                style="atx",
                add_table_of_contents="n",
            )

            ############################################################################
            ### Add about, param, example, etc
            cite_li = self.gen_cite_parameter_strings(func_str=func_str)
            print("cite_li", cite_li)
            if cite_li is not None:
                # joined_ml = "".join(cite_li)
                # print("\n\ncite_li2\n", joined_ml)
                for cparam_str in cite_li:
                    self.mdFile.new_paragraph(cparam_str)

            ############################################################################
            ### Add function code block
            # for func_name, func_str in self.func_text_dict.items():
            ### 1. get func text
            ### 2. trim stuff outside of func
            ### 3. put in code block & write` to md
            cleaned_func_str = self.clean_func_str(multiline_str=func_str)
            # print("cleaned_func_str", cleaned_func_str)
            self.mdFile.insert_code(code=cleaned_func_str, language="bash")

            ############################################################################
            ### Add function dependency block
            multiline_funccalls_input = self.gen_func_dependent_str(func_name=func_name)

            multiline_funccalls_output = None
            print("multiline_funccalls_input", multiline_funccalls_input)
            if multiline_funccalls_input is not None:
                multiline_funccalls_output = draw_tree(
                    parser(multiline_funccalls_input)
                )
                # print("trueeee")
                # sys.exit(0)
            # else:
            #     multiline_funccalls_output = "No functions called."

            # print(
            #     "\nu multiline_funccalls_output\n",
            #     multiline_funccalls_output,
            #     type(multiline_funccalls_output),
            # )
            if multiline_funccalls_output is not None:
                self.mdFile.new_header(
                    level=5,
                    title="Function Calls:",
                    style="atx",
                    add_table_of_contents="n",
                )

                self.mdFile.insert_code(
                    code=multiline_funccalls_output, language="bash"
                )  # new_paragraph(multiline_funccalls_output)  # , language="bash")
            self.mdFile.new_paragraph("\n")

    def write_aliases_section(self):
        self.mdFile.new_header(
            level=2, title="Aliases", style="atx", add_table_of_contents="n"
        )

        mytable = ""
        mytable += "| **Alias Name** | **Code** | **Notes** |\n"
        mytable += "| ------------- | ------------- | ------------- |\n"
        for myalias in self.full_alias_str_list:
            mytable += myalias  # "| **" + ppass + "** | " + pp_dict[stack] + " |\n"

        self.mdFile.new_paragraph(mytable)

    def organise_outfiles_2subdirs(self):
        # probably only does one level
        doc_cats = {
            "aliases": "aliases",
            "completion": "completion",
            "modules": "modules",
            "internal": "internal",
            "completions": "completions",
        }
        cat_substrings = list(doc_cats.keys())

        infile_path_name = self.src_file_path.split("/")
        print("infile_path_name", infile_path_name)

        outfile_name = infile_path_name[-1].replace(".sh", ".md")
        # sys.exit(0)

        full_outfile_path = None
        for cat in cat_substrings:
            if cat in self.src_file_path:
                category = doc_cats.get(cat, None)
                outfile_path = self.out_dir + "/" + category
                mkdir_if_notexists(target=outfile_path)
                full_outfile_path = outfile_path + "/" + outfile_name
                print("full_outfile_path", full_outfile_path)

                return full_outfile_path

        udef_path = self.out_dir + "/" + "undef"
        mkdir_if_notexists(target=udef_path)
        return udef_path + "/" + outfile_name

        # sys.exit(0)

    def main_write_md(self):
        # infile_path_name = self.src_file_path.split("/")
        # outfile_path = self.out_dir + "/" + infile_path_name[-1].replace(".sh", ".md")

        full_outfile_path = self.organise_outfiles_2subdirs()
        print("full_outfile_path", full_outfile_path)
        # sys.exit(0)

        self.mdFile = MdUtils(file_name=full_outfile_path, title=self.cite_about)
        self.mdFile.new_paragraph(f"***(in {self.src_file_path})***")

        ### Process functions
        if len(self.func_text_dict) > 0:
            self.write_func_section()

        ### Process aliases
        if len(self.full_alias_str_list) > 0:
            self.write_aliases_section()

        ### Write out .md file
        self.mdFile.create_md_file()
