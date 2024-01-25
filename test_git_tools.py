import common
import inspect
import logging
import tempfile
import unittest

import git_tools

class TestGitTools(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.tmp_dir = tempfile.TemporaryDirectory()
        logging.info(f"Created temporary directory at '{self.tmp_dir.name}'")

    @classmethod
    def tearDownClass(self):
        logging.info(f"Cleaning temporary directory '{self.tmp_dir.name}'")
        self.tmp_dir.cleanup()

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_is_git_repo_true(self):
        function_name = inspect.getframeinfo(inspect.currentframe()).function
        repo_dir = f"{self.tmp_dir.name}/{function_name}"

        common.create_dir_if_necessary(repo_dir)
        git_tools.run_git_command(repo_dir, "init")
        self.assertTrue(git_tools.is_git_repo(None, None, [repo_dir]))

    def test_is_git_repo_false(self):
        function_name = inspect.getframeinfo(inspect.currentframe()).function
        repo_dir = f"{self.tmp_dir.name}/{function_name}"

        common.create_dir_if_necessary(repo_dir)
        self.assertFalse(git_tools.is_git_repo(None, None, [repo_dir]))

    def _initialize_repo(self, repo_dir):
        """Initialize a git repository with an initial commit.

        To create a branch, git needs at least one commit.

        """

        with open(f"{repo_dir}/README.md", 'w') as file:
            file.write("Hello World!")

        git_tools.run_git_command(repo_dir, "init")
        git_tools.run_git_command(repo_dir, "add README.md")
        git_tools.run_git_command(repo_dir, "commit -m 'Initial commit'")

    def test_is_branch_checked_out_true(self):
        function_name = inspect.getframeinfo(inspect.currentframe()).function
        repo_dir = f"{self.tmp_dir.name}/{function_name}"

        common.create_dir_if_necessary(repo_dir)
        self._initialize_repo(repo_dir)
        git_tools.run_git_command(repo_dir, "checkout -b 'hello'")
        self.assertTrue(git_tools.is_branch_checked_out(None, None,
                                                        [repo_dir, "hello"]))
    def test_is_branch_checked_out_false(self):
        function_name = inspect.getframeinfo(inspect.currentframe()).function
        repo_dir = f"{self.tmp_dir.name}/{function_name}"

        common.create_dir_if_necessary(repo_dir)
        self._initialize_repo(repo_dir)
        git_tools.run_git_command(repo_dir, "checkout -b 'hello'")
        self.assertFalse(git_tools.is_branch_checked_out(None, None,
                                                         [repo_dir, "world"]))

    def test_checkout_branch(self):
        function_name = inspect.getframeinfo(inspect.currentframe()).function
        repo_dir = f"{self.tmp_dir.name}/{function_name}"

        common.create_dir_if_necessary(repo_dir)
        self._initialize_repo(repo_dir)

        git_tools.run_git_command(repo_dir, "branch 'hello'")
        git_tools.checkout_branch(None, None, [repo_dir, "hello"])
        self.assertTrue(git_tools.is_branch_checked_out(None, None,
                                                        [repo_dir, "hello"]))

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
