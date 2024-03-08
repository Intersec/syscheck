from flask import (Blueprint,
                   render_template,
                   session,
                   request,
                   flash,
                   url_for,
                   redirect)
import functools
from workspace import get_workspace

blueprint = Blueprint('db_tools', __name__, url_prefix='/db-tools')

def add_value_to_kv_db(db):
    success = False
    key = request.args.get("key")
    value = request.args.get("value")

    if not key:
        flash("Key is mandatory", "error")

    if not value:
        flash("Value is mandatory", "error")

    if key and value:
        db.set_value(key, value)
        flash(f"Success", "notice")
        success = True

    return success

def remove_value_from_kv_db(db, is_common_db):
    key = request.args.get("key")
    value = request.args.get("value")

    if not key:
        flash("Key is mandatory", "error")
        return False

    if is_common_db == False and key == "task_conf_path":
        flash("Key 'task_conf_path' cannot be removed", "error")
        return False

    db.remove_key(key)
    flash(f"Success", "notice")

    return True

def add_value_to_coll_db(db):
    success = False
    collection = request.args.get("collection")
    value = request.args.get("value")

    if not collection:
        flash("Collection is mandatory", "error")

    if not value:
        flash("Value is mandatory", "error")

    if collection and value:
        db.add_value(collection, value)
        flash(f"Success", "notice")
        success = True

    return success

def remove_collection_from_coll_db(db, is_common_db):
    collection = request.args.get("collection")

    if not collection:
        flash("Collection is mandatory", "error")
        return False

    if is_common_db and collection == "environments":
        flash("Collection 'environments' cannot be removed", "error")
        return False

    db.remove_collection(collection)
    flash(f"Success", "notice")

    return True

def remove_value_from_coll_db(db, is_common_db):
    success = False
    collection = request.args.get("collection")
    value = request.args.get("value")

    if not collection:
        flash("Collection is mandatory", "error")

    if not value:
        flash("Value is mandatory", "error")

    if is_common_db and collection == "environments":
        flash("Collection 'environments' cannot be removed", "error")
        return False

    if collection and value:
        db.remove_value(collection, value)
        flash(f"Success", "notice")
        success = True

    return success

@blueprint.route('/', methods=["GET"])
def page_db_tools():
    env_kv_db = None
    env_collection_db = None

    workspace = get_workspace()

    if session.get("env_name"):
        env = workspace.get_environment(session["env_name"])
        env_kv_db = env.key_value_db
        env_collection_db = env.collection_db

    common_kv_db = workspace.get_key_value_db()
    common_collection_db = workspace.get_collection_db()

    if request.method == "GET":
        if request.args.get("add_env_kv_db_elt"):
            if add_value_to_kv_db(env_kv_db):
                return redirect(url_for("db_tools.page_db_tools",
                                        env_kv_db="set"))

        elif request.args.get("delete_env_kv_db_elt"):
            if remove_value_from_kv_db(env_kv_db, False):
                return redirect(url_for("db_tools.page_db_tools",
                                        env_kv_db="set"))

        elif request.args.get("add_env_coll_db_elt"):
            if add_value_to_coll_db(env_collection_db):
                return redirect(url_for("db_tools.page_db_tools",
                                        env_coll_db="set"))

        elif request.args.get("delete_env_coll_db_coll"):
            if remove_collection_from_coll_db(env_collection_db, False):
                return redirect(url_for("db_tools.page_db_tools",
                                        env_coll_db="set"))

        elif request.args.get("delete_env_coll_db_elt"):
            if remove_value_from_coll_db(env_collection_db, False):
                return redirect(url_for("db_tools.page_db_tools",
                                        env_coll_db="set"))

        elif request.args.get("add_common_kv_db_elt"):
            if add_value_to_kv_db(common_kv_db):
                return redirect(url_for("db_tools.page_db_tools",
                                        common_kv_db="set"))

        elif request.args.get("delete_common_kv_db_elt"):
            if remove_value_from_kv_db(common_kv_db, True):
                return redirect(url_for("db_tools.page_db_tools",
                                        common_kv_db="set"))

        elif request.args.get("add_common_coll_db_elt"):
            if add_value_to_coll_db(common_collection_db):
                return redirect(url_for("db_tools.page_db_tools",
                                        common_coll_db="set"))

        elif request.args.get("delete_common_coll_db_coll"):
            if remove_collection_from_coll_db(common_collection_db, True):
                return redirect(url_for("db_tools.page_db_tools",
                                        common_coll_db="set"))

        elif request.args.get("delete_common_coll_db_elt"):
            if remove_value_from_coll_db(common_collection_db, True):
                return redirect(url_for("db_tools.page_db_tools",
                                        common_coll_db="set"))

    return render_template('db_tools.html',
                           env_kv_db = env_kv_db,
                           env_collection_db = env_collection_db,
                           common_kv_db=common_kv_db,
                           common_collection_db=common_collection_db)
