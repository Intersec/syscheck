import unittest

import db_tools
import test_common

class TestDBTools(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        pass

    @classmethod
    def tearDownClass(self):
        pass

    def setUp(self):
        self.workspace = test_common.FakeWorkspace()
        self.environment = test_common.FakeEnvironment()
        self.task = test_common.FakeTask(self.workspace, self.environment)
        self.env_key_value_db = self.environment.key_value_db
        self.env_collection_db = self.environment.collection_db
        self.common_key_value_db = self.task.get_workspace_key_value_db()
        self.common_collection_db = self.task.get_workspace_collection_db()
        self.requirement = {
            "id": "fake_requirement"
        }

    def tearDown(self):
        pass

    def test_is_set_with_non_existing_key(self):
        self.assertFalse(db_tools.is_set(self.task, self.requirement,
                                         [ "env", "key001" ]))
        self.assertFalse(db_tools.is_set(self.task, self.requirement,
                                         [ "common", "key001" ]))

    def test_is_set_with_existing_key(self):
        self.env_key_value_db.set_value("key001", "value001")
        self.common_key_value_db.set_value("key001", "value001")
        self.assertTrue(db_tools.is_set(self.task, self.requirement,
                                        [ "env", "key001" ]))
        self.assertTrue(db_tools.is_set(self.task, self.requirement,
                                        [ "common", "key001" ]))

    def test_is_set_with_default_key(self):
        self.env_key_value_db.set_value(self.requirement["id"], "value001")
        self.assertTrue(db_tools.is_set(self.task, self.requirement,
                                        [ "env" ]))
        self.assertFalse(db_tools.is_set(self.task, self.requirement,
                                         [ "common" ]))

    def test_is_set_with_default_db_and_key(self):
        self.env_key_value_db.set_value(self.requirement["id"], "value001")
        self.assertTrue(db_tools.is_set(self.task, self.requirement, []))

    def test_set_value(self):
        self.assertFalse(self.env_key_value_db.is_set("key001"))
        db_tools.set_value(self.task, self.requirement,
                           [ "env", "k001", "v001" ])
        db_tools.set_value(self.task, self.requirement,
                           [ "common", "k002", "v002" ])
        self.assertEqual(self.env_key_value_db.get_value("k001"), "v001")
        self.assertEqual(self.common_key_value_db.get_value("k002"), "v002")

    # TODO: add more tests
