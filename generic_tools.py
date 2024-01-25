def is_key_set(task, requirement, args):
    arg_db = "env"
    arg_key = requirement["id"]

    if len(args) >= 2:
        arg_key = args[1]

    if len(args) >= 1:
        arg_env = args[0]

    # TODO add test to check that default values are used (they are not!)
    if args[0] == "env":
        db = task.get_env_key_value_db()
    elif args[0] == "common":
        db = task.get_workspace_key_value_db()

    return db.is_key_set(arg_key)

def each(task, requirement, args):
    for arg in args:
        if not arg:
            return False
    return True

def any(task, requirement, args):
    for arg in args:
        if arg:
            return True
    return False

def true(task, requirement, args):
    return True

def false(task, requirement, args):
    return False

def none(task, requirement, args):
    return None
