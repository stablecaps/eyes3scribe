# import logging
# import os
# import sys

# from mdutils.mdutils import MdUtils
# from rich import print as rprint

# import bashautodoc.helpo.hfile as hfile
# from bashautodoc.DocSectionWriterFunction import DocSectionWriterFunction
# from bashautodoc.models.filepath_datahandler import FilepathDatahandler

# # from rst_to_myst import rst_to_myst


# # from bashautodoc.helpo.hstrops import str_multi_replace

# LOG = logging.getLogger(__name__)


# class RstandM2MdFileWriter:
#     def __init__(
#         self,
#         conf,
#         docdata,
#     ):
#         self.conf = conf
#         #
#         self.docdata = docdata
#         #

#     def process_hwdocs(self):
#         if self.docdata.infile_relpath.endswith(".rst"):
#             pass
#             # rst_text = hfile.read_file_2string(filepath=self.docdata.infile_relpath)
#             # md_text = rst_to_myst(rst_text)
#             # rprint(md_text.text)
