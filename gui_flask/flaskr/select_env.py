import functools

from flask import (Blueprint,
                   render_template,
                   request,
                   flash,
                   redirect,
                   session,
                   url_for)
import sys
from workspace import (get_workspace,
                       EnvironmentExists,
                       EnvironmentNotFound,
                       InvalidEnvironmentName)

blueprint = Blueprint('select_env', __name__, url_prefix='/select-env')

def select_env():
    success = False
    env_name = request.args.get("env_name")

    if not env_name:
        flash("Environment name is mandatory", "error")

    if env_name:
        workspace = get_workspace()

        try:
            workspace.get_environment(env_name)
            session["env_name"] = env_name
            flash(f"Environment '{env_name}' successfully loaded", "notice")
            success = True
        except (InvalidEnvironmentName, EnvironmentNotFound):
            flash(f"Environment '{env_name}' does not exists", "error")

    return success

def common_create_env(env_name, task_path):
    success = False
    workspace = get_workspace()

    try:
        workspace.create_environment(env_name, task_path)
        session["env_name"] = env_name
        workspace.get_collection_db().add_value("known_tasks", task_path)
        flash(f"Environment '{env_name}' successfully created", "notice")
        success = True
    except InvalidEnvironmentName:
        flash(f"Invalid environment name '{env_name}'", "error")
    except FileNotFoundError:
        flash(f"Task file '{env_name}' does not exists", "error")
    except EnvironmentExists:
        flash(f"Environment '{env_name}' already exists", "error")

    return success

def create_env_using_known_task():
    success = False
    env_name = request.args.get("env_name")
    task_path = request.args.get("task_cfg_path")

    if not env_name:
        flash("Environment name is mandatory", "error")

    if not task_path:
        flash("Task file is mandatory", "error")

    if env_name and task_path:
        if common_create_env(env_name, task_path):
            success = True

    return success

def create_env():
    success = False
    env_name = request.args.get("env_name")
    task_path = request.args.get("task_cfg_path")

    if not env_name:
        flash("Environment name is mandatory", "error")

    if not task_path:
        flash("Task file is mandatory", "error")

    if env_name and task_path:
        if common_create_env(env_name, task_path):
            success = True

    return success

@blueprint.route('/', methods=["GET"])
def page_select_env():

    if request.method == "GET":
        if request.args.get("create_env"):
            if create_env():
                return redirect(url_for("select_env.page_select_env"))

        if request.args.get("known_task"):
            if create_env_using_known_task():
                return redirect(url_for("select_env.page_select_env"))

        if request.args.get("select_env"):
            if select_env():
                return redirect(url_for("select_env.page_select_env"))

        if request.args.get("forget_env"):
            session["env_name"] = None
            return redirect(url_for("select_env.page_select_env"))

    workspace = get_workspace()
    tasks_list = workspace.get_collection_db().get_values("known_tasks")
    env_list = workspace.get_environments_list()

    return render_template('select_env.html',
                           tasks_list=tasks_list,
                           env_list=env_list)
