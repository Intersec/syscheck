import json
import os

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

        requirements_file = task_json["requirements_file"]
        if not os.path.isabs(requirements_file):
            task_file_directory = os.path.dirname(task_file)
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

    def get_requirement(self, req_name):
        if req_name not in self.requirements.keys():
            raise InvalidConfiguration(f"Requirement not found '{req_name}'")

        req = self.requirements[req_name]

        return req

    def check_requirement_status(self, req_name):
        def check_requirement_dependencies(req):
            if "dependencies" in req.keys():
                dependencies = req["dependencies"]
                if not type(dependencies) == list:
                    msg = f"Dependencies for '{req['id']}' is not an array"
                    raise InvalidConfiguration(msg)

                for dep in dependencies:
                    if not self.check_requirement_status(dep):
                        return False
            return True

        def run_requirement_auto_check(req):
            auto_check = req["automatic_check"]
            res = requirements.solve_element(self, req, auto_check)

            # Make sure the returned value is a boolean. If it is not, it
            # might be that the configured check function is actually a
            # procedure and the requirement configuration is wrong so better
            # warn the user.
            if type(res) != bool:
                raise NotBool(req["automatic_check"][0])

            return res

        req = self.get_requirement(req_name)

        if not check_requirement_dependencies(req):
            return False

        if not run_requirement_auto_check(req):
            return False

        return True

    def is_task_ready(self):
        return self.check_requirement_status(self.target_requirement_name)

