import os

from collection_database import CollectionDatabase
import common
from environment import Environment
from key_value_database import KeyValueDatabase

class EnvironmentExists(Exception):
    pass

class EnvironmentNotFound(Exception):
    pass

class InvalidEnvironmentName(Exception):
    pass

def get_workspace():
    default_path = os.environ.get("HOME") + "/.local/share/syscheck"
    env_path = os.environ.get("SYSCHECK_DATA_HOME")

    path = None
    if env_path:
        path = env_path
    else:
        path = default_path

    return Workspace(path)

class Workspace():

    def __init__(self, location):
        self.location = location.rstrip("/")

        common.create_dir_if_necessary(self.location)

        key_value_db_location = f"{self.location}/key_value.db"
        self.key_value_db = KeyValueDatabase(key_value_db_location)

        collection_db_location = f"{self.location}/collection.db"
        self.collection_db = CollectionDatabase(collection_db_location)

    def get_key_value_db(self):
        return self.key_value_db

    def get_collection_db(self):
        return self.collection_db

    def get_environments_list(self):
        return self.collection_db.get_values("environments")

    def _check_environment_name(self, env_name):
        for letter in env_name:
            if not (letter.isalnum() or letter == '-' or letter == '_'):
                return False
        return True

    def _get_environment_attributes(self, env_name):
        if not self._check_environment_name(env_name):
            raise InvalidEnvironmentName()

        env_prefix = f"{self.location}/{env_name}"
        env_kv_db_path = f"{env_prefix}_key_value.db"
        env_collection_db_path = f"{env_prefix}_collection.db"

        return env_kv_db_path, env_collection_db_path

    def _get_environment(self, env_name):
        env_list = self.get_environments_list()

        if env_name not in env_list:
            raise EnvironmentNotFound()

        kv_db_path, collection_db_path = self._get_environment_attributes(env_name)

        key_value_db = KeyValueDatabase(kv_db_path)
        collection_db = CollectionDatabase(collection_db_path)
        env = Environment(key_value_db, collection_db)

        return env

    def get_environment(self, env_name):
        if not self._check_environment_name(env_name):
            raise InvalidEnvironmentName()

        env = self._get_environment(env_name)
        return env

    def create_environment(self, env_name, task_conf_path):
        if not self._check_environment_name(env_name):
            raise InvalidEnvironmentName()

        if not os.path.isfile(task_conf_path):
            raise FileNotFoundError(f"Task configuration file {task_conf_path}")

        task_conf_path = os.path.normpath(task_conf_path)
        if not os.path.isabs(task_conf_path):
            task_conf_path = os.path.abspath(task_conf_path)

        if env_name in self.get_environments_list():
            raise EnvironmentExists()

        self.collection_db.add_value("environments", env_name)

        kv_db_path, collection_db_path = self._get_environment_attributes(env_name)

        key_value_db = KeyValueDatabase(kv_db_path)
        collection_db = CollectionDatabase(collection_db_path)

        key_value_db.set_value("task_conf_path", task_conf_path)

        env = Environment(key_value_db, collection_db)

        return env
