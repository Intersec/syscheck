import os
import unittest

from task import Task, NotBool
import test_common

class TestTask(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        pass

    @classmethod
    def tearDownClass(self):
        pass

    def setUp(self):
        self.workspace = test_common.FakeWorkspace()
        self.environment = test_common.FakeEnvironment()
        self.task_cfg_path = test_common.get_test_task_cfg_path()

    def tearDown(self):
        pass

    def test_error_if_configuration_path_not_set(self):
        expected_msg_re = f"^missing key 'task_conf_path' in kv database$"
        with self.assertRaisesRegex(AssertionError, expected_msg_re):
            Task(self.workspace, self.environment)

    def test_error_if_configuration_path_not_absolute(self):
        path = os.path.relpath(self.task_cfg_path['task-001'])
        self.environment.key_value_db.set_value("task_conf_path", path)

        expected_msg_re = f"^{path} is not an absolute path$"
        with self.assertRaisesRegex(AssertionError, expected_msg_re):
            Task(self.workspace, self.environment)

    def test_error_if_task_file_does_not_exists(self):
        path = self.task_cfg_path['do-not-exists']
        self.environment.key_value_db.set_value("task_conf_path", path)
        expected_msg_re = f"Task file '{path}' not found"

        with self.assertRaisesRegex(FileNotFoundError, expected_msg_re):
            Task(self.workspace, self.environment)

    def test_error_if_req_file_does_not_exists(self):
        path = self.task_cfg_path['task-004']
        self.environment.key_value_db.set_value("task_conf_path", path)

        # TODO better set the requirements file path in the expected error
        abs_req_file = os.path.abspath("./do-not-exists.json")
        expected_msg_re = f"Requirements file '{abs_req_file}' not found"

        with self.assertRaisesRegex(FileNotFoundError, expected_msg_re):
            Task(self.workspace, self.environment)

    def test_requirements_in_another_directory(self):
        """This test check that, if the task file links to a requirements file in a
        parent directory, the program will check in the task file's parent
        directory and not in the working direcory's parent directory.

        """

        path = self.task_cfg_path['task-005']
        self.environment.key_value_db.set_value("task_conf_path", path)

        Task(self.workspace, self.environment)

        # If the task was created then the requirment file was found.
        self.assertTrue(True)

    def test_get_target_requirement(self):
        self.environment.key_value_db.set_value("task_conf_path",
                                                self.task_cfg_path['task-001'])
        task = Task(self.workspace, self.environment)
        self.assertEqual(task.get_target_requirement(),
                         "TEST_TASK_001__REQ_TRUE")

    def test_is_ready_return_true(self):
        self.environment.key_value_db.set_value("task_conf_path",
                                                self.task_cfg_path['task-001'])
        task = Task(self.workspace, self.environment)
        self.assertTrue(task.is_task_ready())

    def test_is_ready_return_false(self):
        self.environment.key_value_db.set_value("task_conf_path",
                                                self.task_cfg_path['task-002'])
        task = Task(self.workspace, self.environment)
        self.assertFalse(task.is_task_ready())

    def test_is_ready_throws_not_boot(self):
        self.environment.key_value_db.set_value("task_conf_path",
                                                self.task_cfg_path['task-005'])
        task = Task(self.workspace, self.environment)
        with self.assertRaises(NotBool):
            task.is_task_ready()