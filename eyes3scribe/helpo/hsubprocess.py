"""Subprocess Helper functions."""
import shlex
import subprocess
import sys
from typing import List, Optional, Union


def shlex_convert_str_2list(comm_str: str) -> List[str]:
    """
    Convert a linux command into list format with shlex.
    """

    split_comm = shlex.split(comm_str)

    # remove all instances of empty string
    split_comm_clean = list(filter(lambda a: a != "", split_comm))

    return split_comm_clean


def run_cmd_with_output(comm_str: str) -> Optional[bytes]:
    """
    Run a subprocess command and print error message on failure.
    Also returns output on success and
    False on failure so that it can be handled downstream.
    """

    split_comm_clean = shlex_convert_str_2list(comm_str=comm_str)

    try:
        sp_resp = subprocess.check_output(split_comm_clean)
        return sp_resp
    except Exception as err:
        print(f"\n{err}")
        return None


def run_cmd_with_errorcode(comm_str: str) -> bool:
    """
    Run a subprocess command and print error code on failure.
    Also returns output on success and
    False on failure so that it can be handled downstream.
    """

    split_comm_clean = shlex_convert_str_2list(comm_str=comm_str)

    try:
        subprocess.check_output(split_comm_clean)
    except Exception as err:
        print(f"error code  {err}")
        return False

    return True


def process_subp_output(
    cmd_output: Optional[bytes],
    delimiter: str = "\t",
    exclude_list: Union[List[str], None] = None,
) -> List[List[str]]:
    """
    Preprocesses output from subprocess command and returns a list of lists,
    Each sublist corresponds to a row in the output.
    Delimiter can be specified to split each row.
    Elements in exclude_list are stripped from each row.
    `exclude_list` default is `["", " "]`
    """
    if exclude_list is None:
        exclude_list = ["", " "]

    assert cmd_output, "Error: For process_subp_output(), cmd_output var is None"

    holder = []
    for line in cmd_output.decode().split("\n"):
        # print(line)
        splitty_line = line.split(delimiter)
        # print(splitty_line)
        filtered_line = [
            elem.strip() for elem in splitty_line if elem not in exclude_list
        ]
        if len(filtered_line) > 0:
            holder.append(filtered_line)
    return holder


def check_pipe_errors(proc_step_dict, comm_li):
    for idx in range(len(proc_step_dict)):
        curr_proc = "proc" + str(idx)

        proc_step_dict[curr_proc].wait()

        retcode = proc_step_dict[curr_proc].returncode
        print(curr_proc + " retcode:", retcode)

        proc_step_dict[curr_proc].terminate()

        if retcode != 0:
            print("Failed running: ", comm_li[idx])
            sys.exit(retcode)


def run_cmd_with_pipes(comm_li):
    proc_step_dict = {}
    for idx, comm in enumerate(comm_li):
        curr_proc = "proc" + str(idx)
        print("comm", comm)

        process_args = {
            "args": shlex_convert_str_2list(comm),
            "stdout": subprocess.PIPE,
            "stderr": None,
            "text": True,
        }
        if idx != 0:
            last_proc = "proc" + str(idx - 1)
            process_args["stdin"] = proc_step_dict[last_proc].stdout
        proc_step_dict[curr_proc] = subprocess.Popen(**process_args)

    out, err = proc_step_dict[curr_proc].communicate(timeout=15)
    print("\nout:", len(out), out)
    print("\nerr:", err)

    if len(out) == 0:
        print("\n### Checking Subprocess errors")
        check_pipe_errors(proc_step_dict, comm_li)
    return out
