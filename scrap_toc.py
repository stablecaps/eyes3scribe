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
    for line in filetext.split("\n"):
        # line_stripped = line.strip()
        if not inRecordingMode:
            if "```{toctree}" in line:
                rprint("TRUE: found toctree")
                inRecordingMode = True
                line_holder.append(line)
        elif "```" in line:
            inRecordingMode = False
            line_holder.append(line)
        else:
            line_holder.append(line)

    return line_holder


###########
if __name__ == "__main__":
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

            toc_list_cleaned = [
                line
                for line in toc_list
                if line != "" and "maxdepth:" not in line and "```" not in line
            ]

            print("toc_list_cleaned", toc_list_cleaned)
            # sys.exit(42)

            md_toclink_list = []
            for toc_linkname in toc_list_cleaned:
                file_link_list = hfile.list_matching_files_recursively(
                    search_path=hwdoc_root,
                    myglob=f"{toc_linkname}.md",
                )
                rprint("\nfile_link_list", f"{toc_linkname}.md", file_link_list)

                if len(file_link_list) > 1:
                    print("ERROR: more than one file found")
                    sys.exit(42)

                md_rellink_cleaned = file_link_list[0]  # .replace("./", "")
                md_rellink = f"- [**{toc_linkname.capitalize().replace('/index', '')}**]({md_rellink_cleaned})"
                rprint(
                    "md_rellink",
                )
                md_toclink_list.append(md_rellink)

            print("md_toclink_list", md_toclink_list)

            joined_original_toclinks = "\n".join(toc_list)
            rprint("\njoined_original_toclinks\n", joined_original_toclinks)

            joined_toclinks = "\n".join(md_toclink_list)
            rprint("\njoined_toclinks\n", joined_toclinks)
            # sys.exit(42)

            print("\n\n")

            replaced_filetext = filetext.replace(
                joined_original_toclinks, joined_toclinks
            )
            print("replaced_filetext\n", replaced_filetext)
            sys.exit(42)
