import logging
import system_tools
import test_common
import unittest

class TestSystemTools(unittest.TestCase):

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

    def test_read_file(self):
        filename = "./test-simple-file.txt"
        expected_content = "Hello.\nWorld.\n"
        read_content = system_tools.read_file(None, None, [filename])
        self.assertEqual(read_content, expected_content)

    def test_read_file_without_arguments(self):
        with self.assertRaises(ValueError):
            read_content = system_tools.read_file(None, None, [])

    def test_concat_str(self):
        args = [ "Hello", " ", "World!" ]
        expected_result = "Hello World!"
        result = system_tools.concat_str(None, None, args)
        self.assertEqual(result, expected_result)

    def test_binary_exists_success(self):
        bin_name = "ls"
        self.assertTrue(system_tools.binary_exists(None, None, [bin_name]))

    def test_binary_exists_fails(self):
        bin_name = "sdfghjk"    # Let's hope it doesn't exists on the system
        self.assertFalse(system_tools.binary_exists(None, None, [bin_name]))

    def test_binary_exists_with_no_arguments(self):
        with self.assertRaises(ValueError):
            system_tools.binary_exists(None, None, [])

    #TODO: add tests for the other system_tools functions.
