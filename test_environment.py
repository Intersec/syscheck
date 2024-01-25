import unittest

from environment import Environment
import test_common

class TestEnvironment(unittest.TestCase):

    def test_db_are_accessible(self):
        """Environment is quite simple, it only store the databases so this test makes
        sure that the object provided to the constructor can be retrieved.

        """
        fake_db_1 = "fake_db_1"
        fake_db_2 = "fake_db_2"
        env = Environment(fake_db_1, fake_db_2)
        self.assertEqual(env.key_value_db, "fake_db_1")
        self.assertEqual(env.collection_db, "fake_db_2")

