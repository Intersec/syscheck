import common
import git_tools
import os
from requirements import InvalidElement
from task import Task, NotBool, InvalidConfiguration
import tempfile
import test_common
import unittest

class TestTask(unittest.TestCase):
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

    def test_error_if_configuration_path_not_set(self):
        expected_msg_re = f"^missing key 'task_conf_path' in kv database$"
        with self.assertRaisesRegex(AssertionError, expected_msg_re):
            Task(self.workspace, self.environment)

    def test_error_if_configuration_path_not_absolute(self):
        path = os.path.relpath(self.task_cfg_path['task-001'])
        self.environment.key_value_db.set_value("task_conf_path", path)

        expected_msg_re = f"^{path} is not an absolute path$"
        with self.assertRaisesRegex(AssertionError, expected_msg_re):
            Task(self.workspace, self.environment)

    def test_error_if_task_file_does_not_exists(self):
        path = self.task_cfg_path['do-not-exists']
        self.environment.key_value_db.set_value("task_conf_path", path)
        expected_msg_re = f"Task file '{path}' not found"

        with self.assertRaisesRegex(FileNotFoundError, expected_msg_re):
            Task(self.workspace, self.environment)

    def test_error_if_req_file_does_not_exists(self):
        path = self.task_cfg_path['task-004']
        self.environment.key_value_db.set_value("task_conf_path", path)

        # TODO better set the requirements file path in the expected error
        abs_req_file = os.path.abspath("./do-not-exists.json")
        expected_msg_re = f"Requirements file '{abs_req_file}' not found"

        with self.assertRaisesRegex(FileNotFoundError, expected_msg_re):
            Task(self.workspace, self.environment)

    def test_requirements_in_another_directory(self):
        """Test loading requirements in another directory

        This test check that, if the task file links to a requirements file in
        a parent directory, the program will check in the task file's parent
        directory and not in the working direcory's parent directory.

        """

        path = self.task_cfg_path['task-005']
        self.environment.key_value_db.set_value("task_conf_path", path)

        Task(self.workspace, self.environment)

        # If the task was created then the requirement file was found.
        self.assertTrue(True)

    def test_get_target_requirement_name(self):
        task = self._get_task("task-001")
        self.assertEqual(task.get_target_requirement_name(),
                         "TEST_TASK_001__REQ_TRUE")

    def test_get_requirement(self):
        task = self._get_task("task-001")
        req = task.get_requirement("TEST_TASK_001__REQ_TRUE")
        self.assertEqual(req["id"], "TEST_TASK_001__REQ_TRUE")
        self.assertEqual(req["label"], "Automatic check returns true")
        self.assertEqual(req["automatic_check"][0], "generic_tools.true")

    def test_is_ready_return_true(self):
        task = self._get_task("task-001")
        self.assertTrue(task.is_task_ready())

    def test_is_ready_return_false(self):
        task = self._get_task("task-002")
        self.assertFalse(task.is_task_ready())

    def test_is_ready_throws_not_boot(self):
        task = self._get_task("task-005")
        with self.assertRaises(NotBool):
            task.is_task_ready()

    def test_dependency_is_true_but_auto_check_is_false(self):
        task = self._get_task("task-001")
        self.assertFalse(
            task.check_requirement_status("TEST_TASK_001__REQ_DEP_TRUE"))

    def test_auto_check_is_false_using_req_obj(self):
        task = self._get_task("task-001")
        req = task.requirements["TEST_TASK_001__REQ_FALSE"]
        self.assertFalse(task.check_requirement_status(req))

    def test_auto_check_is_true_using_req_obj(self):
        task = self._get_task("task-001")
        req = task.requirements["TEST_TASK_001__REQ_TRUE"]
        self.assertTrue(task.check_requirement_status(req))

    def test_auto_check_is_not_a_function(self):
        task = self._get_task("task-001")

        fun = "TEST_TASK_001__REQ_FALSE"
        expected_msg_re = f"^Cannot extract module and function from '{fun}'$"
        with self.assertRaisesRegex(InvalidElement, expected_msg_re):
            task.check_requirement_status(
                "TEST_TASK_001__REQ_INVAL_AUTO_CHECK_001")

    def test_dependency_do_not_exists(self):
        task = self._get_task("task-001")
        expected_msg_re = f"^Requirement not found 'REQ_DO_NOT_EXISIS'$"
        with self.assertRaisesRegex(InvalidConfiguration, expected_msg_re):
            task.check_requirement_status("TEST_TASK_001__REQ_INVAL_DEP_002")

    def test_requirement_do_not_exists(self):
        task = self._get_task("task-001")
        expected_msg_re = f"^Requirement not found 'REQ_DO_NOT_EXISIS'$"
        with self.assertRaisesRegex(InvalidConfiguration, expected_msg_re):
            task.check_requirement_status("REQ_DO_NOT_EXISIS")

    def test_auto_check_is_true_but_dependency_is_false(self):
        task = self._get_task("task-001")
        self.assertFalse(
            task.check_requirement_status("TEST_TASK_001__REQ_DEP_FALSE"))

    def test_both_dependencies_and_auto_check_are_true(self):
        task = self._get_task("task-001")
        self.assertTrue(
            task.check_requirement_status(
                "TEST_TASK_001__REQ_DEP_AND_CHECK_TRUE"))

    def test_auto_check_returns_none(self):
        task = self._get_task("task-001")
        with self.assertRaises(NotBool):
            task.check_requirement_status("TEST_TASK_001__REQ_NO_RESULT")

    def test_dependecies_checked_using_requirement_object(self):
        task = self._get_task("task-001")
        req = task.requirements["TEST_TASK_001__REQ_DEP_TRUE"]
        self.assertTrue(task.check_requirement_dependencies(req))

    def test_dependecies_not_checked_using_requirement_object(self):
        task = self._get_task("task-001")
        req = task.requirements["TEST_TASK_001__REQ_DEP_FALSE"]
        self.assertFalse(task.check_requirement_dependencies(req))

    def test_dependecies_checked_using_requirement_name(self):
        task = self._get_task("task-001")
        req_id = "TEST_TASK_001__REQ_DEP_TRUE"
        self.assertTrue(task.check_requirement_dependencies(req_id))

    def test_dependecies_not_checked_using_requirement_name(self):
        task = self._get_task("task-001")
        req_id = "TEST_TASK_001__REQ_DEP_FALSE"
        self.assertFalse(task.check_requirement_dependencies(req_id))

    def test_dependecies_not_checked_using_requirement_name(self):
        task = self._get_task("task-001")
        req_id = "TEST_TASK_001__REQ_DEP_FALSE"
        self.assertFalse(task.check_requirement_dependencies(req_id))

    def test_dependecies_checked_using_any(self):
        task = self._get_task("task-001")
        req_id = "TEST_TASK_001__REQ_DEP_LIST_ANY_TRUE"
        self.assertTrue(task.check_requirement_dependencies(req_id))

    def test_dependecies_not_checked_using_any(self):
        task = self._get_task("task-001")
        req_id = "TEST_TASK_001__REQ_DEP_LIST_ANY_FALSE"
        self.assertFalse(task.check_requirement_dependencies(req_id))

    def test_dependecies_checked_using_each(self):
        task = self._get_task("task-001")
        req_id = "TEST_TASK_001__REQ_DEP_LIST_EACH_TRUE"
        self.assertTrue(task.check_requirement_dependencies(req_id))

    def test_dependecies_not_checked_using_each(self):
        task = self._get_task("task-001")
        req_id = "TEST_TASK_001__REQ_DEP_LIST_EACH_FALSE"
        self.assertFalse(task.check_requirement_dependencies(req_id))

    def test_complex_dependecies_checked(self):
        task = self._get_task("task-001")
        req_id = "TEST_TASK_001__REQ_DEP_COMPLEX_EACH_TRUE"
        self.assertTrue(task.check_requirement_dependencies(req_id))

    def test_complex_dependecies_not_checked(self):
        task = self._get_task("task-001")
        req_id = "TEST_TASK_001__REQ_DEP_COMPLEX_EACH_FALSE"
        self.assertFalse(task.check_requirement_dependencies(req_id))

    def test_auto_res_with_dependencies_not_met(self):
        task = self._get_task("task-001")
        req_id = "TEST_TASK_001__SIMPLE_AUTO_RES"
        expected_msg = f"Requirement '{req_id}' dependencies are not ready"
        with self.assertRaisesRegex(AssertionError, expected_msg):
            task.apply_automatic_resolution(req_id, "auto")

    def test_auto_res_using_req_obj_with_dependencies_not_met(self):
        task = self._get_task("task-001")
        req = task.requirements["TEST_TASK_001__SIMPLE_AUTO_RES"]
        expected_msg = f"Requirement '{req['id']}' dependencies are not ready"
        with self.assertRaisesRegex(AssertionError, expected_msg):
            task.apply_automatic_resolution(req["id"], "auto")

    def test_auto_check_with_dependencies_not_met(self):
        task = self._get_task("task-001")
        # The automatic check will raise a NotBool exception if it is run so
        # if no exception is raised this is that the automatic check was
        # indeed not run.
        task.check_requirement_status("TEST_TASK_001__REQ_DEP_BUT_NO_RESULT")

    def test_safe_auto_check_true(self):
        task = self._get_task("task-001")
        req_id = "TEST_TASK_001__REQ_SAFE_CHECK_SUCCESS_001"
        self.assertTrue(task.check_requirement_status(req_id))

    def test_safe_auto_check_false_but_auto_check_true(self):
        task = self._get_task("task-001")
        req_id = "TEST_TASK_001__REQ_SAFE_CHECK_SUCCESS_002"
        self.assertTrue(task.check_requirement_status(req_id))

    def test_safe_auto_check_false_and_no_auto_check(self):
        task = self._get_task("task-001")
        req_id = "TEST_TASK_001__REQ_SAFE_CHECK_NO_AUTO_CHECK_FAIL_001"
        self.assertFalse(task.check_requirement_status(req_id))

    def test_safe_auto_check_false_and_dependency_fails(self):
        task = self._get_task("task-001")
        req_id = "TEST_TASK_001__REQ_SAFE_CHECK_FAIL_002"
        self.assertFalse(task.check_requirement_status(req_id))

    def test_dependency_good_but_safe_auto_check_and_auto_check_false(self):
        task = self._get_task("task-001")
        req_id = "TEST_TASK_001__REQ_SAFE_CHECK_FAIL_003"
        self.assertFalse(task.check_requirement_status(req_id))

    def test_auto_res(self):
        def initialize_repo(repo_dir):
            """Initialize a directory with a git repository

            If the repository doesn't have a valid commit, creating a branch
            with 'git branch <branchname>' fails.

            This function creates a git repository with a commit in an
            existing directory to avoid this issue.

            """
            with open(f"{repo_dir}/README.md", 'w') as file:
                file.write("Hello World!")

            git_tools.run_git_command(repo_dir, "init")
            git_tools.run_git_command(repo_dir, "add README.md")
            git_tools.run_git_command(repo_dir, "commit -m 'Initial commit'")

        task = self._get_task("task-001")
        req = task.requirements["TEST_TASK_001__SIMPLE_AUTO_RES"]
        db = task.get_env_key_value_db()
        target_branch = "release-0.1"
        source_branch = "release-0.2"

        tmp_dir = tempfile.TemporaryDirectory()
        repo_path = tmp_dir.name

        try:
            db.set_value("TEST_TASK_001__SIMPLE_AUTO_RES_REPO_PATH",
                         repo_path)
            db.set_value("TEST_TASK_001__SIMPLE_AUTO_RES_REPO_BRANCH",
                         target_branch)
            initialize_repo(repo_path);
            git_tools.run_git_command(repo_path, f"branch '{target_branch}'")
            git_tools.run_git_command(repo_path, f"branch '{source_branch}'")
            git_tools.checkout_branch(None, None,
                                      [ repo_path, source_branch ])
            assert git_tools.is_branch_checked_out(
                None, None, [ repo_path, source_branch ]), "Invalid branch"
            task.apply_automatic_resolution(req, "auto")
            self.assertTrue(
                git_tools.is_branch_checked_out(
                    None, None, [ repo_path, target_branch ]))
        finally:
            tmp_dir.cleanup()

    def test_auto_res_with_wrong_method(self):
        task = self._get_task("task-001")

        req_id = "TEST_TASK_001__AUTO_RES_DB"
        res_id = "manual"
        with self.assertRaisesRegex(
                InvalidConfiguration,
                f"Requirement resolution '{req_id}.{res_id}' not automatic"):
            task.apply_automatic_resolution(req_id, res_id)

    def test_auto_res_with_no_steps(self):
        task = self._get_task("task-001")

        req_id = "TEST_TASK_001__AUTO_RES_DB"
        res_id = "auto_no_steps"
        with self.assertRaisesRegex(
                InvalidConfiguration,
                f"Requirement resolution '{req_id}.{res_id}' has no steps"):
            task.apply_automatic_resolution(req_id, res_id)

    def test_auto_res_with_invalid_id(self):
        task = self._get_task("task-001")

        req_id = "TEST_TASK_001__AUTO_RES_DB"
        res_id = "key_do_not_exists"
        with self.assertRaisesRegex(
                InvalidConfiguration,
                f"Requirement resolution '{req_id}.{res_id}' do not exists"):
            task.apply_automatic_resolution(req_id, res_id)
