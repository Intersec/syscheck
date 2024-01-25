import logging
import os
import unittest

from key_value_database import KeyValueDatabase
import test_common

class TestKeyValueDatabase(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.db_path = test_common.get_temporary_filename()
        logging.info("Database will be stored in '%s'", self.db_path)

    @classmethod
    def tearDownClass(self):
        logging.info("Removing database file '%s'", self.db_path)
        os.unlink(self.db_path)

    def setUp(self):
        logging.info("Cleaning database content (%s)", self.db_path)
        test_common.clear_database_file(self.db_path)
        self.database = KeyValueDatabase(self.db_path)

    def tearDown(self):
        pass

    def test_get_key_from_empty_db(self):
        self.assertEqual(self.database.get_value("key01"), None)

    def test_get_key_from_non_empty_db(self):
        self.database.set_value("key01", "v1")
        self.assertEqual(self.database.get_value("key02"), None)

    def test_set_then_get_return_the_same_value(self):
        self.database.set_value("key01", "v1")
        self.assertEqual(self.database.get_value("key01"), "v1")

    def test_update_value(self):
        self.database.set_value("key01", "v1")
        self.assertEqual(self.database.get_value("key01"), "v1")
        self.database.set_value("key01", "v2")
        self.assertEqual(self.database.get_value("key01"), "v2")

    def test_is_set_from_empty_db(self):
        self.assertEqual(self.database.is_set("key01"), False)

    def test_is_set_with_non_existing_key_from_non_empty_db(self):
        self.database.set_value("key01", "v1")
        self.assertEqual(self.database.is_set("key02"), False)

    def test_is_set_with_existing_key(self):
        self.database.set_value("key01", "v1")
        self.assertEqual(self.database.is_set("key01"), True)

    def test_remove_key_with_existing_key(self):
        self.database.set_value("key01", "v1")
        self.assertEqual(self.database.is_set("key01"), True)
        self.database.remove_key("key01")
        self.assertEqual(self.database.is_set("key01"), False)

    def test_remove_key_with_removed_key(self):
        self.assertEqual(self.database.is_set("key01"), False)
        self.database.remove_key("key01")
        self.assertEqual(self.database.is_set("key01"), False)

# logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    unittest.main()

# Running:
#
# python -m unittest test_key_value_database
#
# Other examples:
#
# python -m unittest test_module1 test_module2
# python -m unittest test_module.TestClass
# python -m unittest test_module.TestClass.test_method
# python -m unittest tests/test_something.py # Remove the '.py' suffix
