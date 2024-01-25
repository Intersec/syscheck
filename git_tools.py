import os

class GitException(Exception):
    def __init__(self, message, status, output = None):
        self.message = message
        self.status = status
        self.output = output

def run_git_command(repo_dir, cmd_args, capture_output = False):
    full_command = f"git -C {repo_dir} {cmd_args}"

    # FIXME stderr is displayed and shouldn't be.

    # Use os.popen instead of os.system to:
    #   * Hide the process output;
    #   * Allow output capture;
    process = os.popen(full_command)

    output = process.readlines()

    # If the process returned zero, the close() function will return None,
    # otherwise the value will represent the error code returned by the
    # process or the signal number that interrupted it.
    status = process.close()

    if status:
        if status > 0:
            status = status >> 1
        raise GitException(full_command, status, output);

    result = output if capture_output else None

    return result

def is_git_repo(task, requirement, args):
    if len(args) < 1:
        raise ValueError("Not enough arguments")

    repo_dir = args[0]

    try:
        run_git_command(repo_dir, "rev-parse")
        repo_exists = True
    except GitException:
        repo_exists = False

    return repo_exists

def is_branch_checked_out(task, requirement, args):
    if len(args) < 2:
        raise ValueError("Not enough arguments")

    repo_dir = args[0]
    branch_name = args[1]

    out = run_git_command(repo_dir, "rev-parse --abbrev-ref HEAD", True)
    assert len(out) == 1, \
        f"Expected single line when checking current branch, got '{out}'"

    return out[0].rstrip() == branch_name

def is_tag_checked_out(task, requirement, args):
    if len(args) < 2:
        raise ValueError("Not enough arguments")

    repo_dir = args[0]
    tag_name = args[1]

    out = run_git_command(repo_dir, "describe --tags", True)
    assert len(out) == 1, \
        f"Expected single line when checking current branch, got '{out}'"

    return out[0].rstrip() == tag_name

def checkout_branch(task, requirement, args):
    if len(args) < 2:
        raise ValueError("Not enough arguments")

    repo_dir = args[0]
    branch_name = args[1]

    run_git_command(repo_dir, f"checkout {branch_name}")
