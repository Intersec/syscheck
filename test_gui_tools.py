import gui_tools
import logging
import os
import sys
import test_common
import unittest

class TestGuiTools(unittest.TestCase):

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

    def test_format_description_one_substitution(self):
        workspace = test_common.FakeWorkspace()
        env = test_common.FakeEnvironment()
        task = test_common.FakeTask(workspace, env)
        task.get_env_key_value_db().set_value("name", "Léon")
        description = "Hello [<name>|env.name]"
        new_description = gui_tools.format_description(description, task)
        self.assertEqual(new_description, "Hello Léon")

    def test_format_description_two_substitutions(self):
        workspace = test_common.FakeWorkspace()
        env = test_common.FakeEnvironment()
        task = test_common.FakeTask(workspace, env)
        task.get_env_key_value_db().set_value("first", "Léon")
        task.get_env_key_value_db().set_value("last", "Dupont")
        description = "Hello [<firstname>|env.first] [<lastname>|env.last]"
        new_description = gui_tools.format_description(description, task)
        self.assertEqual(new_description, "Hello Léon Dupont")

    def test_format_description_one_default_value(self):
        workspace = test_common.FakeWorkspace()
        env = test_common.FakeEnvironment()
        task = test_common.FakeTask(workspace, env)
        task.get_env_key_value_db().set_value("first", "Léon")
        description = "Hello [<firstname>|env.first] [<lastname>|env.last]"
        new_description = gui_tools.format_description(description, task)
        self.assertEqual(new_description, "Hello Léon <lastname>")

    def test_format_description_two_patterns_glued(self):
        workspace = test_common.FakeWorkspace()
        env = test_common.FakeEnvironment()
        task = test_common.FakeTask(workspace, env)
        description = "Hello [<firstname>|env.first][<lastname>|env.last]"
        new_description = gui_tools.format_description(description, task)
        self.assertEqual(new_description, "Hello <firstname><lastname>")

    def test_format_description_with_escaped_char(self):
        workspace = test_common.FakeWorkspace()
        env = test_common.FakeEnvironment()
        task = test_common.FakeTask(workspace, env)
        description = "Hello [<firstname>|env.first] \[<lastname>|env.last]"
        new_description = gui_tools.format_description(description, task)
        self.assertEqual(new_description,
                         "Hello <firstname> \[<lastname>|env.last]")

if __name__ == '__main__':
    unittest.main()
