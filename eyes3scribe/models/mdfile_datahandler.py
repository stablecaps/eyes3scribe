# import logging
# from dataclasses import dataclass

# from mdutils.mdutils import MdUtils

# # from eyes3scribe.DocSectionWriterFunction import DocSectionWriterFunction
# from eyes3scribe.function_dependency_processor import FunctionDependencyProcessor
# from eyes3scribe.models.function_datahandler import FunctionDataHolder

# LOG = logging.getLogger(__name__)


# # TODO: enable slots=True
# # @dataclass(slots=True)
# @dataclass()
# class MDFileDataHolder:
#     mdFile: MdUtils = None


# class MDFileDatahandler:
#     def __new__(
#         cls, srcfile_rpath, mdfile_name: str, title: str, funcdata: FunctionDataHolder
#     ):
#         # https://stackoverflow.com/questions/2491819/how-to-return-a-value-from-init-in-python
#         cls.mddata = MDFileDataHolder()
#         cls.funcdata = funcdata

#         cls.mddata.mdFile = MdUtils(
#             file_name=mdfile_name,
#             title=title.capitalize(),
#         )

#         cls.srcfile_rpath = srcfile_rpath

#         return cls.main()

#     def _add_about_param_example_etc(self, func_str):
#         """
#         Add information about parameters and examples to the markdown file.

#         Args:
#             func_str (str): The function string.

#         Example:
#             writer._add_about_param_example_etc('my_function')
#         """
#         cite_li = self._gen_cite_parameter_strings(func_str=func_str)
#         # if cite_li:
#         if len(cite_li) > 0:
#             LOG.debug("cite_li %s", cite_li)
#             # sys.exit(42)
#             for cparam_str in cite_li:
#                 self.mdFile.new_paragraph(cparam_str)

#     @classmethod
#     def _write_page_header(cls, func_name):
#         """
#         Write the page header to the markdown file.

#         Args:
#             func_name (str): The name of the function.

#         Example:
#             writer._write_page_header('my_function')
#         """
#         cls.mddata.new_paragraph("******")
#         cls.mddata.new_header(
#             level=3, title=f">> {func_name}():", style="atx", add_table_of_contents="n"
#         )

#     @classmethod
#     def main(cls):
#         cls.mddata.new_paragraph(f"***(in {cls.srcfile_rpath})***")

#         if len(cls.funcdata.func_text_dict) > 0:
#             for func_name, func_str in cls.funcdata.func_text_dict.items():
#                 LOG.debug("\n*~~~~~\n %s", func_name)  # , "\n", func_str)
#                 cls._write_page_header(func_name)
#                 cls._add_about_param_example_etc(func_str)
#             # doc_section_writer_function = DocSectionWriterFunction(
#             #     mdFile=cls.mddata,
#             #     func_text_dict=self.func_text_dict,
#             #     func_dep_dict=self.func_dep_dict,
#             #     cite_parameters=self.func_def_keywords,
#             # )
#             # doc_section_writer_function.write_func_section()

#         return cls.mddata
