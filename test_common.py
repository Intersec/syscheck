import os
import tempfile

from collection_volatile_database import CollectionVolatileDatabase
from key_value_volatile_database import KeyValueVolatileDatabase

class FakeWorkspace():
    def __init__(self, key_value_db = None, collection_db = None):
        if not key_value_db:
            key_value_db = KeyValueVolatileDatabase()

        if not collection_db:
            collection_db = CollectionVolatileDatabase()

        self.key_value_db = key_value_db
        self.collection_db = collection_db

class FakeEnvironment():
    def __init__(self, key_value_db = None, collection_db = None):
        if not key_value_db:
            key_value_db = KeyValueVolatileDatabase()

        if not collection_db:
            collection_db = CollectionVolatileDatabase()

        self.key_value_db = key_value_db
        self.collection_db = collection_db

def get_temporary_filename():
    """Return the path to an empty file that can be modified at will.

    This functions uses tempfile.NamedTemporaryFile to create the
    file. It will then close it because the database should be
    normally-closed when it is not accessed but it will make sure that
    the file is not removed yet.

    This file is expected to be deleted when the test ends. It could
    be removed like this:
    >>> os.unlink(filename)
    """
    f = tempfile.NamedTemporaryFile("w", delete=False)
    f.close()
    return f.name

def clear_database_file(filename):
    """Overwrite file content with an empty dictonnary"""
    with open(filename, 'w') as file:
        file.write("{}")

def get_test_task_cfg_path():
        file_dir = os.path.dirname(__file__)

        test_task_cfg = {
            "task-001": os.path.join(file_dir, "test-task-001.json"),
            "task-002": os.path.join(file_dir, "test-task-002.json"),
            "task-003": os.path.join(file_dir, "test-task-003.json"),
            "do-not-exists": os.path.join(file_dir, "do-not-exists.json"),
            "task-004": os.path.join(file_dir, "test-task-004.json"),
            "task-005": os.path.join(file_dir, "test-dir/test-task-005.json"),
        }

        return test_task_cfg
