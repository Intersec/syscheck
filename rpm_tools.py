import os

def extract_rpm(task, env, args):
    if len(args) != 2:
        usage = "extract_rpm <directory> <RPM path>"
        raise ValueError(f"Not enough arguments: {usage}")

    directory = args[0]
    rpm_path = args[1]

    assert os.path.isdir(directory), f"{direcory} is not a directory"
    assert os.path.isfile(rpm_path), f"{rpm_path} is not a file"

    res = os.system(f"cd {directory}; rpm2cpio '{rpm_path}' | cpio -idmv")

    if res != 0:
        raise Exception("Failed to extract RPM", res)
