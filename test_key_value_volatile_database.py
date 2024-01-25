import logging
import os
import unittest

from key_value_volatile_database import KeyValueVolatileDatabase
import test_common

class TestKeyValueVolatileDatabase(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        pass

    @classmethod
    def tearDownClass(self):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_file_not_created(self):
        """Test that no files are created.
        
        The location of the database is in the root directory with a path that
        is unlikely to exists.

        If the database tries to create a file at this place, it would raise
        an error because of missing rights.

        """
        db = KeyValueVolatileDatabase("/sys-check-file-that-cannot-be-created")

        # At this time, the database file of the original KeyValueDatabase is
        # created when the object is created. This second step handle the case
        # where the file would be created only when a value is stored in the
        # database.
        db.set_value("key001", "value001")

    def test_set_and_get(self):
        db = KeyValueVolatileDatabase("/sys-check-file-that-cannot-be-created")
        db.set_value("key001", "value001")
        self.assertEqual(db.get_value("key001"), "value001")

    def test_is_set_is_true(self):
        db = KeyValueVolatileDatabase("/sys-check-file-that-cannot-be-created")
        db.set_value("key001", "value001")
        self.assertTrue(db.is_set("key001"))

    def test_is_set_is_false(self):
        db = KeyValueVolatileDatabase("/sys-check-file-that-cannot-be-created")
        self.assertFalse(db.is_set("key001"))

    def test_is_set_with_removed_key(self):
        db = KeyValueVolatileDatabase("/sys-check-file-that-cannot-be-created")
        db.set_value("key001", "value001")
        db.remove_key("key001")
        self.assertFalse(db.is_set("key001"))
