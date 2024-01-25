import json
import os
import sys

import environment
import requirements

class DupplicateRequirement(Exception):
    pass

class InvalidConfiguration(Exception):
    pass

class NotBool(Exception):
    pass

class NotAbsolute(Exception):
    pass

class Task():
    def __init__(self, workspace, environment):
        self.workspace = workspace
        self.environment = environment

        if not self.environment.key_value_db.is_set("task_conf_path"):
            # At this time, the environment is created by the workspace and
            # this environment should contain in the KeyValueDatabase the path
            # to the task configuration file.
            raise AssertionError(f"missing key 'task_conf_path' in kv database")

        task_file = self.environment.key_value_db.get_value("task_conf_path")
        if not os.path.isabs(task_file):
            # The path in the databse should be absolute. At this time, the
            # Workspace class is the only class that can create environment,
            # and thus, it's databases. It should have made sure that the path
            # was absolute.
            raise AssertionError(f"{task_file} is not an absolute path")

        try:
            with open(task_file) as json_file:
                task_json = json.load(json_file)
        except FileNotFoundError:
            raise FileNotFoundError(f"Task file '{task_file}' not found")

        self.id = task_json["id"]
        self.target_requirement_name = task_json["requirement"]

        task_file_directory = os.path.dirname(task_file)

        requirements_file = task_json["requirements_file"]
        if not os.path.isabs(requirements_file):
            requirements_file = os.path.join(task_file_directory, requirements_file)

        try:
            with open(requirements_file) as json_file:
                requirements = json.load(json_file)
        except FileNotFoundError:
            # Clean file path for the error message.
            requirements_file = os.path.normpath(requirements_file)
            raise FileNotFoundError(f"Requirements file '{requirements_file}' not found")

        self.requirements = {}
        for requirement in requirements:
            if requirement["id"] in self.requirements:
                raise DupplicateRequirement(requirement["id"])
            self.requirements[requirement["id"]] = requirement

        if task_json.get("libraries_paths"):
            lib_paths = task_json["libraries_paths"]
            for path in lib_paths:
                if not os.path.isabs(path):
                    path = os.path.join(task_file_directory, path)
                if not path in sys.path:
                    sys.path.append(path)

    def get_target_requirement_name(self):
        return self.target_requirement_name

    def get_env_key_value_db(self):
        return self.environment.key_value_db

    def get_env_collection_db(self):
        return self.environment.collection_db

    def get_workspace_key_value_db(self):
        return self.workspace.key_value_db

    def get_workspace_collection_db(self):
        return self.workspace.collection_db

    def get_requirement(self, req_id):
        if req_id not in self.requirements.keys():
            raise InvalidConfiguration(f"Requirement not found '{req_id}'")

        req = self.requirements[req_id]

        return req

    def check_requirement_dependencies(self, req_arg):
        """Check if the dependecies of the requirement are met.

        The req_arg parameter can be the requirement's name or the requirement
        itself.

        """

        def check_dependencies(dependencies):
            if type(dependencies) == str:
                return self.check_requirement_status(dependencies)

            elif type(dependencies) == list:
                if len(dependencies) < 2:
                    msg = f"Expect at least a method and an element"
                    raise InvalidConfiguration(msg, dependencies)

                method = dependencies[0]

                elts = []
                for elt in dependencies[1:]:
                    elts.append(check_dependencies(elt))

                if method == "any":
                    return True in elts
                elif method == "each":
                    return not False in elts
                else:
                    msg = f"Invalid dependency method"
                    raise InvalidConfiguration(msg, method, dependencies)
            else:
                msg = f"Unexpected type of dependencies"
                raise InvalidConfiguration(msg, dependencies)

        if type(req_arg) is str:
            req = self.get_requirement(req_arg)
        else:
            req = req_arg

        if "dependencies" not in req.keys():
            # Dependencies are good if there are none.
            return True

        return check_dependencies(req["dependencies"])

    def apply_automatic_resolution(self, req_arg, res_id):
        """Apply a requirement's automatic resolution.

        The req_arg parameter can be the requirement's name or the requirement
        itself.

        The res_id parameter is the resolution identifier specified as the
        resolution's key in the configuration.

        """

        if type(req_arg) is str:
            req = self.get_requirement(req_arg)
        else:
            req = req_arg

        req_id = req['id']

        if res_id not in req["resolution"].keys():
            raise InvalidConfiguration(
                f"Requirement resolution '{req_id}.{res_id}' do not exists")

        auto_res = req["resolution"][res_id]

        if auto_res["method"] != "automatic":
            raise InvalidConfiguration(
                f"Requirement resolution '{req_id}.{res_id}' not automatic")

        if "steps" not in auto_res.keys():
            raise InvalidConfiguration(
                f"Requirement resolution '{req_id}.{res_id}' has no steps")

        if ("safe" not in auto_res) or (auto_res["safe"] is False):
            if not self.check_requirement_dependencies(req):
                raise AssertionError(
                    f"Requirement '{req_id}' dependencies are not ready")

        res = requirements.solve_element(self, req, auto_res["steps"])

    def check_requirement_status(self, req_arg):
        def run_requirement_auto_check(req):
            return run_requirement_check(req, "automatic_check")

        def run_requirement_safe_auto_check(req):
            return run_requirement_check(req, "safe_automatic_check")

        def run_requirement_check(req, item):
            auto_check = req[item]
            res = requirements.solve_element(self, req, auto_check)

            # Make sure the returned value is a boolean. If it is not, it
            # might be that the configured check function is actually a
            # procedure and the requirement configuration is wrong so better
            # warn the user.
            if type(res) != bool:
                raise NotBool(req[item][0])

            return res

        if type(req_arg) is str:
            req = self.get_requirement(req_arg)
        else:
            req = req_arg

        if "safe_automatic_check" in req:
            if run_requirement_safe_auto_check(req):
                return True

        if "automatic_check" in req:
            if self.check_requirement_dependencies(req):
                if run_requirement_auto_check(req):
                    return True

        return False

    def is_task_ready(self):
        return self.check_requirement_status(self.target_requirement_name)

