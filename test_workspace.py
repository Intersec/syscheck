import inspect
import logging
import os
import tempfile
import unittest

from collection_database import CollectionDatabase
from key_value_database import KeyValueDatabase
import test_common
from workspace import (Workspace,
                       EnvironmentExists,
                       EnvironmentNotFound,
                       InvalidEnvironmentName)

class TestWorkspace(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.tmp_dir = tempfile.TemporaryDirectory()
        logging.info(f"Created temporary directory at '{self.tmp_dir.name}'")

        current_file_directory = os.path.dirname(__file__)
        if current_file_directory == "":
            # If there was no directory part, then the file is in the current
            # directory.
            current_file_directory = "."

        self.task_cfg_path = test_common.get_test_task_cfg_path()

    @classmethod
    def tearDownClass(self):
        logging.info(f"Cleaning temporary directory '{self.tmp_dir.name}'")
        self.tmp_dir.cleanup()

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_workspace_dir_creation(self):
        function_name = inspect.getframeinfo(inspect.currentframe()).function
        workspace_location = f"{self.tmp_dir.name}/{function_name}"

        workspace = Workspace(workspace_location)
        self.assertTrue(os.path.isdir(workspace_location))

    def test_databases_are_accessible(self):
        function_name = inspect.getframeinfo(inspect.currentframe()).function
        workspace_location = f"{self.tmp_dir.name}/{function_name}"

        workspace = Workspace(workspace_location)
        self.assertIsInstance(workspace.key_value_db, KeyValueDatabase)
        self.assertIsInstance(workspace.collection_db, CollectionDatabase)

    def test_key_value_db_path(self):
        function_name = inspect.getframeinfo(inspect.currentframe()).function
        workspace_location = f"{self.tmp_dir.name}/{function_name}"

        workspace = Workspace(workspace_location)
        self.assertTrue(os.path.isfile(f"{workspace_location}/key_value.db"))

    def test_collection_db_path(self):
        function_name = inspect.getframeinfo(inspect.currentframe()).function
        workspace_location = f"{self.tmp_dir.name}/{function_name}"

        workspace = Workspace(workspace_location)
        self.assertTrue(os.path.isfile(f"{workspace_location}/collection.db"))

    def test_workspace_path_is_trimmed(self):
        function_name = inspect.getframeinfo(inspect.currentframe()).function
        workspace_location = f"{self.tmp_dir.name}/{function_name}"

        # Add a trailing '/' in the workspace location and check it doesn't
        # change the directory's name and the databases path.
        workspace = Workspace(workspace_location + "/")
        self.assertTrue(os.path.isdir(workspace_location))
        self.assertTrue(os.path.isfile(f"{workspace_location}/key_value.db"))
        self.assertTrue(os.path.isfile(f"{workspace_location}/collection.db"))

    def test_collection_updated_at_environment_creation(self):
        function_name = inspect.getframeinfo(inspect.currentframe()).function
        workspace_location = f"{self.tmp_dir.name}/{function_name}"

        workspace = Workspace(workspace_location)
        self.assertListEqual(workspace.get_environments_list(), [])

        workspace.create_environment("new-env", self.task_cfg_path["task-001"])
        self.assertListEqual(workspace.get_environments_list(), ["new-env"])

    def test_environment_creation_databases_created(self):
        function_name = inspect.getframeinfo(inspect.currentframe()).function
        workspace_location = f"{self.tmp_dir.name}/{function_name}"

        workspace = Workspace(workspace_location)
        workspace.create_environment("new-env", self.task_cfg_path["task-001"])
        self.assertTrue(os.path.isfile(f"{workspace_location}/new-env_key_value.db"))
        self.assertTrue(os.path.isfile(f"{workspace_location}/new-env_collection.db"))

    def test_create_env_using_name_with_dot(self):
        function_name = inspect.getframeinfo(inspect.currentframe()).function
        workspace_location = f"{self.tmp_dir.name}/{function_name}"

        workspace = Workspace(workspace_location)

        with self.assertRaises(InvalidEnvironmentName):
            workspace.create_environment("new.env", self.task_cfg_path["task-001"])

    def test_create_env_using_name_with_slash(self):
        function_name = inspect.getframeinfo(inspect.currentframe()).function
        workspace_location = f"{self.tmp_dir.name}/{function_name}"

        workspace = Workspace(workspace_location)

        with self.assertRaises(InvalidEnvironmentName):
            workspace.create_environment("new/env", self.task_cfg_path["task-001"])

    def test_create_env_using_name_with_escaped_slash(self):
        function_name = inspect.getframeinfo(inspect.currentframe()).function
        workspace_location = f"{self.tmp_dir.name}/{function_name}"

        workspace = Workspace(workspace_location)

        with self.assertRaises(InvalidEnvironmentName):
            workspace.create_environment("new\/env", self.task_cfg_path["task-001"])

    def test_create_dupplicate_env(self):
        function_name = inspect.getframeinfo(inspect.currentframe()).function
        workspace_location = f"{self.tmp_dir.name}/{function_name}"

        workspace = Workspace(workspace_location)

        workspace.create_environment("new-env", self.task_cfg_path["task-001"])
        with self.assertRaises(EnvironmentExists):
            workspace.create_environment("new-env", self.task_cfg_path["task-001"])

    def test_get_existing_env(self):
        function_name = inspect.getframeinfo(inspect.currentframe()).function
        workspace_location = f"{self.tmp_dir.name}/{function_name}"

        workspace = Workspace(workspace_location)
        env_create = workspace.create_environment("new-env", self.task_cfg_path["task-001"])
        env_get = workspace.get_environment("new-env")

        # The object returned by the workspace.get_environment is not the same
        # object returned by workspace.create_environment because both
        # functions creates a new instance of the Environment class using also
        # new instances of it's databases class wich uses the same files.
        #
        # To assert that both Environment object represents the same
        # environment we use one database to confirm that modifying the
        # database of the first environment modifies the database of the
        # second environment.
        self.assertFalse(env_get.key_value_db.is_set("key001"))
        env_create.key_value_db.set_value("key001", "value001")
        self.assertEqual(env_get.key_value_db.get_value("key001"), "value001")

    def test_get_not_existing_env(self):
        function_name = inspect.getframeinfo(inspect.currentframe()).function
        workspace_location = f"{self.tmp_dir.name}/{function_name}"

        workspace = Workspace(workspace_location)
        with self.assertRaises(EnvironmentNotFound):
            workspace.get_environment("new-env")

    def test_environment_task_path_is_absolute(self):
        function_name = inspect.getframeinfo(inspect.currentframe()).function
        workspace_location = f"{self.tmp_dir.name}/{function_name}"

        workspace = Workspace(workspace_location)
        env = workspace.create_environment("new-env", self.task_cfg_path["task-001"])
        with self.assertRaises(ValueError):
            env.key_value_db.get_value("task_conf_path").index("test-dir")

    def test_create_environment_task_do_not_exists(self):
        function_name = inspect.getframeinfo(inspect.currentframe()).function
        workspace_location = f"{self.tmp_dir.name}/{function_name}"

        workspace = Workspace(workspace_location)
        with self.assertRaises(FileNotFoundError):
            env = workspace.create_environment("new-env",
                                               self.task_cfg_path["do-not-exists"])

    def test_environment_task_path_is_normalized(self):
        """The task-002 configuration contains a non-straight path with the directory
        test-dir that is not required. This checks that the path stored in the
        database doesn't use that part.

        The path in the database is supposed to be absolute so there are no
        attempt for an exact match.

        """
        function_name = inspect.getframeinfo(inspect.currentframe()).function
        workspace_location = f"{self.tmp_dir.name}/{function_name}"

        workspace = Workspace(workspace_location)
        env = workspace.create_environment("new-env", self.task_cfg_path["task-002"])
        self.assertTrue(os.path.isabs(env.key_value_db.get_value("task_conf_path")))
