import os

def create_dir_if_necessary(path):
    try:
        os.mkdir(path, mode=0o755)
    except FileExistsError:
        pass
