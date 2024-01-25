import os
import shutil
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

def mkdir(task, requirement, args):
    if len(args) != 1:
        usage = "mkdir <path>"
        raise ValueError(f"Not enough arguments: {usage}")

    path = args[0]

    os.mkdir(path)

def copy_file(task, requirement, args):
    if len(args) != 2:
        usage = "copy_file <src> <dst>"
        raise ValueError(f"Not enough arguments: {usage}")

    src = args[0]
    dst = args[1]

    shutil.copy(src, dst)

def set_file_mode(task, requirement, args):
    if len(args) != 2:
        usage = "set_file_mode <file> <mode str>"
        raise ValueError(f"Not enough arguments: {usage}")

    path = args[0]
    mode_str = args[1]

    mode_int = int(mode_str, 8)

    os.chmod(path, mode_int)

def test_file_access(task, requirement, args):
    if len(args) != 2:
        usage = "test_file_access <file> <mode>"
        raise ValueError(f"Not enough arguments: {usage}")

    path = args[0]
    mode_arg = args[1]

    mode = 0
    if "R" in mode_arg:
        mode = mode | os.R_OK
    if "W" in mode_arg:
        mode = mode | os.W_OK
    if "X" in mode_arg:
        mode = mode | os.X_OK

    os.access(path, mode)
