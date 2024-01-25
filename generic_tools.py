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

def compare(task, requirement, args):
    if len(args) != 2:
        usage = "compare <first value> <second value>"
        raise ValueError(f"Not enough arguments: {usage}")

    v1 = args[0]
    v2 = args[1]

    return v1 == v2
