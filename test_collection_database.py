import logging
import os
import unittest

from collection_database import CollectionDatabase
import test_common

class TestCollectionDatabase(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.db_path = test_common.get_temporary_filename()
        logging.info("Database will be stored in '%s'", self.db_path)

    @classmethod
    def tearDownClass(self):
        logging.info("Removing database file '%s'", self.db_path)
        os.unlink(self.db_path)

    def setUp(self):
        def clear_database_file(filename):
            with open(filename,'w') as file:
                file.write("{}")

        logging.info("Cleaning database content (%s)", self.db_path)
        clear_database_file(self.db_path)
        self.database = CollectionDatabase(self.db_path)

    def tearDown(self):
        pass

    def test_get_values_from_empty_db(self):
        self.assertListEqual(self.database.get_values("collection001"), [])

    def test_get_values_from_db_with_one_element(self):
        self.database.add_value("collection001", "v1")
        self.assertListEqual(self.database.get_values("collection001"), ["v1"])

    def test_get_values_from_db_with_two_elements(self):
        self.database.add_value("collection001", "v1")
        self.database.add_value("collection001", "v2")
        self.assertListEqual(self.database.get_values("collection001"), ["v1", "v2"])

    def test_get_values_from_db_with_multiple_collections(self):
        self.database.add_value("collection001", "v1")
        self.database.add_value("collection001", "v2")
        self.database.add_value("collection002", "v3")
        self.assertListEqual(self.database.get_values("collection001"), ["v1", "v2"])
        self.assertListEqual(self.database.get_values("collection002"), ["v3"])
        self.assertListEqual(self.database.get_values("collection003"), [])

    def test_values_are_uniq_in_a_collection(self):
        self.database.add_value("collection001", "v1")
        self.database.add_value("collection001", "v2")
        self.database.add_value("collection001", "v1")
        self.assertListEqual(self.database.get_values("collection001"), ["v1", "v2"])

    def test_removing_the_last_element(self):
        self.database.add_value("collection001", "v1")
        self.database.remove_value("collection001", "v1")
        self.assertListEqual(self.database.get_values("collection001"), [])

    def test_removing_the_not_last_element(self):
        self.database.add_value("collection001", "v1")
        self.database.add_value("collection001", "v2")
        self.database.remove_value("collection001", "v1")
        self.assertListEqual(self.database.get_values("collection001"), ["v2"])

    def test_removing_a_collection(self):
        self.database.add_value("collection001", "v1")
        self.database.add_value("collection001", "v2")
        self.database.remove_collection("collection001")
        self.assertListEqual(self.database.get_values("collection001"), [])

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
