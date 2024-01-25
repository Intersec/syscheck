def _get_key_value_db(task, arg_db):
    if arg_db == "env":
        db = task.get_env_key_value_db()
    elif arg_db == "common":
        db = task.get_workspace_key_value_db()
    else:
        raise ValueError(f"Invalid DB '{arg_db}', expect 'env' or 'common'")

    return db

def _get_collection_db(task, arg_db):
    if arg_db == "env":
        db = task.get_env_collection_db()
    elif arg_db == "common":
        db = task.get_workspace_collection_db()
    else:
        raise ValueError(f"Invalid DB {arg_db}, expect 'env' or 'common'")

    return db

def is_set(task, requirement, args):
    arg_db = "env"
    arg_key = requirement["id"]

    if len(args) >= 1:
        arg_db = args.pop(0)

    if len(args) >= 1:
        arg_key = args.pop(0)

    db = _get_key_value_db(task, arg_db)

    return db.is_set(arg_key)

def set_value(task, requirement, args):
    """Set/replace/reset a key in a Key/Value database

    To remove the value of a key, use "generic_tools.none" as last argument.

    Possible usages:

        * Specify the database, the key and the value:
            * [ "db_tools.set_value", "env|common", "key", "value" ]
        * Use the requirement's ID as the key:
            * [ "db_tools.set_value", "env|common", "value" ]
        * Use the 'env' database and the requirement's ID as the key:
            * [ "db_tools.set_value", "value" ]
        * Remove the key with the requirement's ID from the 'env' database:
            * [ "db_tools.set_value", [ "generic_tools.none" ] ]

    """
    arg_db = "env"
    arg_key = requirement["id"]

    if len(args) < 1:
        raise ValueError("Not enough arguments: set_value [db] [key] value")

    arg_value = args.pop()

    if len(args) >= 1:
        arg_db = args.pop(0)

    if len(args) >= 1:
        arg_key = args.pop(0)

    db = _get_key_value_db(task, arg_db)

    if arg_value == None:
        db.remove_key(arg_key)
    else:
        db.set_value(arg_key, arg_value)

def get_value(task, requirement, args):
    arg_db = "env"
    arg_key = requirement["id"]

    if len(args) >= 1:
        arg_db = args.pop(0)

    if len(args) >= 1:
        arg_key = args.pop(0)

    db = _get_key_value_db(task, arg_db)
    return db.get_value(arg_key)

def add_one_value(task, requirement, args):
    arg_db = "env"
    arg_collection = requirement["id"]

    if len(args) < 1:
        raise ValueError(
            "Not enough arguments: add_one_value [db] [collection] value")

    arg_value = args.pop()

    if len(args) >= 1:
        arg_db = args.pop(0)

    if len(args) >= 1:
        arg_collection = args.pop(0)

    db = _get_collection_db(task, arg_db)
    db.add_value(arg_collection, arg_value)

def add_values(task, requirement, args):
    arg_db = "env"
    arg_collection = requirement["id"]

    if len(args) < 1:
        raise ValueError(
            "Not enough arguments: add_one_value [db] [collection] value")

    arg_value = args.pop()

    if len(args) >= 1:
        arg_db = args.pop(0)

    if len(args) >= 1:
        arg_collection = args.pop(0)

    db = _get_collection_db(task, arg_db)
    for value in arg_value:
        db.add_value(arg_collection, arg_value)

def remove_one_value(task, requirement, args):
    arg_db = "env"
    arg_collection = requirement["id"]

    if len(args) < 1:
        raise ValueError(
            "Not enough arguments: remove_one_value [db] [collection] value")

    arg_value = args.pop()

    if len(args) >= 1:
        arg_db = args.pop(0)

    if len(args) >= 1:
        arg_collection = args.pop(0)

    db = _get_collection_db(task, arg_db)
    db.remove_value(arg_collection, arg_value)

def remove_collection(task, requirement, args):
    arg_db = "env"
    arg_collection = requirement["id"]

    if len(args) >= 1:
        arg_db = args.pop(0)

    if len(args) >= 1:
        arg_collection = args.pop(0)

    db = _get_collection_db(task, arg_db)
    db.remove_collection(arg_collection)

def get_values(task, requirement, args):
    arg_db = "env"
    arg_collection = requirement["id"]

    if len(args) >= 1:
        arg_db = args.pop(0)

    if len(args) >= 1:
        arg_collection = args.pop(0)

    db = _get_collection_db(task, arg_db)
    return db.get_values(arg_collection)

