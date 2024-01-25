import os
import tempfile

def directory_exists(task, requirement, args):

    if len(args) != 1:
        raise ValueError("Not enough arguments: directory_exists <path>")

    path = args.pop()

    return os.path.isdir(path)

def regular_file_exists(task, requirement, args):

    if len(args) != 1:
        raise ValueError("Not enough arguments: regular_file_exists <path>")

    path = args.pop()

    return os.path.isfile(path)

def create_tmp_dir(task, requirement, args):

    suffix = None
    prefix = None
    dir = None

    if len(args) == 3:
        suffix = args[0]
        prefix = args[1]
        dir = args[2]

    if len(args) > 0 and len(args) != 3:
        usage = "create_tmp_dir [suffix prefix dir]"
        raise ValueError(f"Not enough arguments: {usage}")

    tmp_dir = tempfile.mkdtemp(suffix, prefix, dir)

    return tmp_dir

def read_file(task, requirement, args):
    def read_file(filename):
        with open(filename, "r") as f:
            content = f.read()
        return content

    if len(args) != 1:
        usage = "read_file <file path>"
        raise ValueError(f"Not enough arguments: {usage}")

    file_path = args[0]

    content = read_file(file_path)

    return content

def concat_str(task, requirement, args):
    out = "".join(args)
    return out

def binary_exists(task, requirement, args):
    if len(args) != 1:
        usage = "binary_exists <binary name>"
        raise ValueError(f"Not enough arguments: {usage}")

    bin_name = args[0]

    res = os.system(f"which {bin_name}")

    return res == 0

def is_mounted(task, requirement, args):
    if len(args) != 1:
        usage = "is_mounted <mountpoint>"
        raise ValueError(f"Not enough arguments: {usage}")

    mountpoint = args[0]
    if not os.path.isabs(mountpoint):
        mountpoint = os.path.abspath(mountpoint)

    res = os.system(f"mount | grep ' on {mountpoint}'")

    return res == 0
