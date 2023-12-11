import logging
import sys
from collections import defaultdict

from rich import print as rprint

import bashautodoc.helpo.hfile as hfile

# from bashautodoc.helpo.hstrops import search_list_4pattern
from bashautodoc.helpo.hsubprocess import run_cmd_with_output
from bashautodoc.models.filepath_datahandler import FilepathDatahandler


def extract_lines_between_tags(filetext):
    line_holder = []
    inRecordingMode = False
    blank_linecount = 0
    for line in filetext.split("\n"):
        line_stripped = line.strip()
        # print("line", line)
        if not inRecordingMode:
            if "```{toctree}" in line:
                rprint("TRUE: found toctree")
                inRecordingMode = True
                # line_holder.append(line)
        ### Recording stops if 2 blank lines are encountered
        ### or naturally at the end of the file
        elif line_stripped == "```":
            # blank_linecount += 1
            # if blank_linecount == 2:
            #     blank_linecount = 0
            # inRecordingMode = False
            inRecordingMode = False
        else:
            if (line_stripped != "") and "maxdepth:" not in line_stripped:
                line_holder.append(line_stripped)

    return line_holder


###########
hwdoc_relpaths = hfile.search_directory_with_multiple_globs(
    search_path="./docs_bash-it/docs/docshw/",
    glob_patt_list=["*.md"],
)

rprint("hwdoc_relpaths: %s", hwdoc_relpaths)


for hwdoc_relpath in hwdoc_relpaths:
    rprint("\nhwdoc_relpath", hwdoc_relpath)
    hwdoc_root, hwdoc_extension = hwdoc_relpath.rsplit("/", 1)
    rprint("\nhwdoc_root", hwdoc_root, hwdoc_extension)
    # sys.exit(42)
    if "index" in hwdoc_relpath:
        rprint("\nhwdoc_relpath", hwdoc_relpath)
        filetext = hfile.read_file_2string(filepath=hwdoc_relpath)
        # rprint("\nfiletext: %s", filetext)

        rprint("\n\n")

        toc_list = extract_lines_between_tags(filetext=filetext)
        rprint("\ntoc_list: %s", toc_list)

        for item in toc_list:
            file_link_list = hfile.list_matching_files_recursively(
                search_path=hwdoc_root,
                myglob=f"{item}.md",
            )
            rprint("\nfile_link_list", f"{item}.md", file_link_list)

        sys.exit(42)
