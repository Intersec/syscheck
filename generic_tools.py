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
