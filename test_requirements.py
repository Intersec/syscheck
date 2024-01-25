import unittest

from collection_volatile_database import CollectionVolatileDatabase
from key_value_volatile_database import KeyValueVolatileDatabase
import requirements
from task import Task
import test_common

class TestRequirement(unittest.TestCase):
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

    def _get_task(self, task_name_from_cfg):
        task_path = self.task_cfg_path[task_name_from_cfg]
        self.environment.key_value_db.set_value("task_conf_path", task_path)

        return Task(self.workspace, self.environment)

    def test_basic_element_true(self):
        task = self._get_task("task-001")
        req = task.requirements["TEST_TASK_001__REQ_TRUE"]
        self.assertTrue(requirements.solve_element(task, req,
                                                   req["automatic_check"]))

    def test_basic_element_false(self):
        task = self._get_task("task-001")
        req = task.requirements["TEST_TASK_001__REQ_FALSE"]
        self.assertFalse(requirements.solve_element(task, req,
                                                    req["automatic_check"]))

    def test_empty_element(self):
        task = self._get_task("task-001")
        req = task.requirements["TEST_TASK_001__REQ_EMPTY"]
        self.assertTrue(requirements.solve_element(task, req,
                                                   req["automatic_check"]))

    def test_element_each_false(self):
        task = self._get_task("task-001")
        req = task.requirements["TEST_TASK_001__REQ_EACH_FALSE"]
        self.assertFalse(requirements.solve_element(task, req,
                                                    req["automatic_check"]))

    def test_element_each_true(self):
        task = self._get_task("task-001")
        req = task.requirements["TEST_TASK_001__REQ_EACH_TRUE"]
        self.assertTrue(requirements.solve_element(task, req,
                                                   req["automatic_check"]))

    def test_element_any_false(self):
        task = self._get_task("task-001")
        req = task.requirements["TEST_TASK_001__REQ_ANY_FALSE"]
        self.assertFalse(requirements.solve_element(task, req,
                                                    req["automatic_check"]))

    def test_element_any_true(self):
        task = self._get_task("task-001")
        req = task.requirements["TEST_TASK_001__REQ_ANY_TRUE"]
        self.assertTrue(requirements.solve_element(task, req,
                                                   req["automatic_check"]))

    def test_key_value_database_access(self):
        task = self._get_task("task-001")
        req_id = "TEST_TASK_001__REQ_KV_DB_ACCESS"
        kv_db = task.get_env_key_value_db()
        req = task.requirements["TEST_TASK_001__REQ_KV_DB_ACCESS"]

        kv_db.set_value(req_id, "Hello world!")
        self.assertTrue(requirements.solve_element(task, req,
                                                   req["automatic_check"]))

        kv_db.remove_key(req_id)
        self.assertFalse(requirements.solve_element(task, req,
                                                    req["automatic_check"]))
