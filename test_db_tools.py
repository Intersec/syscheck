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
        db_tools.set_value(self.task, self.requirement,
                           [ "env", "k001", "v001" ])
        db_tools.set_value(self.task, self.requirement,
                           [ "common", "k002", "v002" ])
        self.assertEqual(self.env_key_value_db.get_value("k001"), "v001")
        self.assertEqual(self.common_key_value_db.get_value("k002"), "v002")

    def test_unset_value(self):
        self.env_key_value_db.set_value("key001", "value001")
        db_tools.set_value(self.task, self.requirement,
                           [ "env", "key001", None ])
        self.assertFalse(self.env_key_value_db.is_set("k001"))

        self.common_key_value_db.set_value("key002", "value002")
        db_tools.set_value(self.task, self.requirement,
                           [ "common", "key002", None ])
        self.assertFalse(self.common_key_value_db.is_set("k002"))

    def test_set_value_with_default_key(self):
        db_tools.set_value(self.task, self.requirement, [ "env", "v001" ])
        self.assertEqual(
            self.env_key_value_db.get_value(self.requirement["id"]), "v001")

        db_tools.set_value(self.task, self.requirement, [ "common", "v002" ])
        self.assertEqual(
            self.common_key_value_db.get_value(self.requirement["id"]),
            "v002")

    def test_set_value_with_default_db_and_key(self):
        db_tools.set_value(self.task, self.requirement, [ "v001" ])
        self.assertEqual(
            self.env_key_value_db.get_value(self.requirement["id"]),
            "v001")
        self.assertFalse(
            self.common_key_value_db.is_set(self.requirement["id"]))

    def test_set_value_without_value(self):
        """Check an exception is raised when no arguments are provided.

        Also check that the function's usage is provided in the exception's
        message.

        """
        expected_msg = "Not enough arguments: set_value \[db\] \[key\] value"
        with self.assertRaisesRegex(ValueError, expected_msg):
            db_tools.set_value(self.task, self.requirement, [])

    def test_get_value(self):
        self.env_key_value_db.set_value("k001", "v001")
        self.assertEqual(
            db_tools.get_value(
                self.task, self.requirement, [ "env", "k001" ]),
            "v001")

        self.common_key_value_db.set_value("k002", "v002")
        self.assertEqual(
            db_tools.get_value(
                self.task, self.requirement, [ "common", "k002" ]),
            "v002")

    def test_get_value_with_default_key(self):
        self.env_key_value_db.set_value(self.requirement["id"], "v001")
        self.assertEqual(
            db_tools.get_value(
                self.task, self.requirement, [ "env" ]),
            "v001")

        self.common_key_value_db.set_value(self.requirement["id"], "v002")
        self.assertEqual(
            db_tools.get_value(
                self.task, self.requirement, [ "common" ]),
            "v002")

    def test_get_value_with_default_db_and_key(self):
        self.env_key_value_db.set_value(self.requirement["id"], "v001")
        self.assertEqual(
            db_tools.get_value(
                self.task, self.requirement, []),
            "v001")

    def test_add_one_value(self):
        db_tools.add_one_value(self.task, self.requirement,
                               [ "env", "k001", "v001" ])
        self.assertEqual(
            self.env_collection_db.get_values("k001"),
            [ "v001" ])

        db_tools.add_one_value(self.task, self.requirement,
                               [ "common", "k002", "v002" ])
        self.assertEqual(
            self.common_collection_db.get_values("k002"),
            [ "v002" ])

    def test_add_one_value_twice(self):
        db_tools.add_one_value(self.task, self.requirement,
                               [ "env", "k001", "v001" ])
        self.assertEqual(
            self.env_collection_db.get_values("k001"),
            [ "v001" ])

        db_tools.add_one_value(self.task, self.requirement,
                               [ "env", "k001", "v002" ])
        self.assertEqual(
            self.env_collection_db.get_values("k001"),
            [ "v001",  "v002" ])

    def test_add_one_value_with_default_key(self):
        db_tools.add_one_value(self.task, self.requirement, [ "env", "v001" ])
        self.assertEqual(
            self.env_collection_db.get_values(self.requirement["id"]),
            [ "v001" ])

        db_tools.add_one_value(self.task, self.requirement,
                               [ "common", "v002" ])
        self.assertEqual(
            self.common_collection_db.get_values(self.requirement["id"]),
            [ "v002" ])

    def test_add_one_value_with_default_db_and_key(self):
        db_tools.add_one_value(self.task, self.requirement, [ "v001" ])
        self.assertEqual(
            self.env_collection_db.get_values(self.requirement["id"]),
            [ "v001" ])
        self.assertEqual(
            self.common_collection_db.get_values(self.requirement["id"]), [])

    def test_add_value_without_value(self):
        """Check an exception is raised when no arguments are provided.

        Also check that the function's usage is provided in the exception's
        message.

        """
        expected_msg = (
            "Not enough arguments: add_one_value \[db\] \[collection\] value")
        with self.assertRaisesRegex(ValueError, expected_msg):
            db_tools.add_one_value(self.task, self.requirement, [])

    def test_remove_one_value(self):
        self.env_collection_db.add_value("k001", "v001")
        db_tools.remove_one_value(self.task, self.requirement,
                                  [ "env", "k001", "v001" ])
        self.assertEqual(self.env_collection_db.get_values("k001"), [])

        self.common_collection_db.add_value("k002", "v002")
        db_tools.remove_one_value(self.task, self.requirement,
                                  [ "env", "k002", "v002" ])
        self.assertEqual(self.env_collection_db.get_values("k002"), [])

    def test_remove_one_value_with_default_key(self):
        self.env_collection_db.add_value(self.requirement["id"], "v001")
        db_tools.remove_one_value(self.task, self.requirement,
                                  [ "env", "v001" ])
        self.assertEqual(
            self.env_collection_db.get_values(self.requirement["id"]), [])

        self.common_collection_db.add_value(self.requirement["id"], "v002")
        db_tools.remove_one_value(self.task, self.requirement,
                                  [ "common", "v002" ])
        self.assertEqual(
            self.common_collection_db.get_values(self.requirement["id"]), [])

    def test_remove_one_value_with_default_db_and_key(self):
        self.env_collection_db.add_value(self.requirement["id"], "v001")
        self.common_collection_db.add_value(self.requirement["id"], "v001")

        db_tools.remove_one_value(self.task, self.requirement, [ "v001" ])

        self.assertEqual(
            self.env_collection_db.get_values(self.requirement["id"]), [])
        self.assertEqual(
            self.common_collection_db.get_values(self.requirement["id"]),
            [ "v001" ])

    def test_remove_collection(self):
        self.env_collection_db.add_value("k001", "v001")
        db_tools.remove_collection(self.task, self.requirement,
                                   [ "env", "k001" ])
        self.assertEqual(self.env_collection_db.get_values("k001"), [])

        self.common_collection_db.add_value("k002", "v002")
        db_tools.remove_collection(self.task, self.requirement,
                                  [ "env", "k002" ])
        self.assertEqual(self.env_collection_db.get_values("k002"), [])

    def test_remove_collection_with_default_key(self):
        self.env_collection_db.add_value(self.requirement["id"], "v001")
        db_tools.remove_collection(self.task, self.requirement,
                                   [ "env" ])
        self.assertEqual(
            self.env_collection_db.get_values(self.requirement["id"]), [])

        self.common_collection_db.add_value(self.requirement["id"], "v002")
        db_tools.remove_collection(self.task, self.requirement,
                                   [ "common" ])
        self.assertEqual(
            self.common_collection_db.get_values(self.requirement["id"]), [])

    def test_remove_collection_with_default_db_and_key(self):
        self.env_collection_db.add_value(self.requirement["id"], "v001")
        self.common_collection_db.add_value(self.requirement["id"], "v001")

        db_tools.remove_collection(self.task, self.requirement, [])

        self.assertEqual(
            self.env_collection_db.get_values(self.requirement["id"]), [])
        self.assertEqual(
            self.common_collection_db.get_values(self.requirement["id"]),
            [ "v001" ])

    def test_get_values(self):
        self.env_collection_db.add_value("k001", "v001")
        self.assertEqual(
            db_tools.get_values(
                self.task, self.requirement, [ "env", "k001" ]),
            [ "v001" ])

        self.common_collection_db.add_value("k002", "v002")
        self.assertEqual(
            db_tools.get_values(
                self.task, self.requirement, [ "common", "k002" ]),
            [ "v002" ])

    def test_get_values_with_default_key(self):
        self.env_collection_db.add_value(self.requirement["id"], "v001")
        self.assertEqual(
            db_tools.get_values(
                self.task, self.requirement, [ "env" ]),
            [ "v001" ])

        self.common_collection_db.add_value(self.requirement["id"], "v002")
        self.assertEqual(
            db_tools.get_values(
                self.task, self.requirement, [ "common" ]),
            [ "v002" ])

    def test_get_values_with_default_db_and_key(self):
        self.env_collection_db.add_value(self.requirement["id"], "v001")
        self.assertEqual(
            db_tools.get_values(
                self.task, self.requirement, []),
            [ "v001" ])
