import functools

from flask import (Blueprint,
                   render_template,
                   session,
                   flash,
                   url_for,
                   request,
                   redirect)
import db_tools
from .breadcrumb import Breadcrumb
from markupsafe import Markup
from task import Task, InvalidConfiguration
from workspace import get_workspace

blueprint = Blueprint('env', __name__, url_prefix='/env')

def append_class(classes, new_class):
    if len(classes) > 0:
        return "{} {}".format(classes, new_class)
    else:
        return new_class

def get_tree_anchor(tree_id):
    if tree_id:
        return 'tree-id-{}'.format(tree_id)
    else:
        return None

def run_auto_res(task, req_id):
    success = False
    res_id = request.args.get("res_id")

    if not res_id:
        flash("Resolution ID is mandatory", "error")
        return success

    try:
        task.apply_automatic_resolution(req_id, res_id)
        flash("Resolution successfully applied", "notice")
        success = True
    except AssertionError as err:
        # TODO check message to make sure it's a dependency error
        flash("Dependencies are not ready", "error")
    except InvalidConfiguration as err:
        # TODO add exception's message to the flash
        flash("Configuration error", "error")

    return success

def check_user_input_resolution(task, req, res_id):
    success = True

    resolutions = req.get("resolution")
    if not resolutions:
        flash("No resolutions for this requirement", "error")
        return False

    if not res_id:
        flash(f"Reolution ID is mandatory", "error")
        return False

    res = resolutions.get(res_id)
    if not resolutions:
        flash(f"Resolution {res_id} does not exists", "error")
        return False

    db = res.get("db")
    if not db:
        success = False
        flash(f"Database absent from configuration", "error")

    key = res.get("key")
    if not key:
        success = False
        flash(f"Key absent from configuration", "error")

    return success

def set_value_from_user(task, req_id):
    success = True

    value = request.args.get("user_value")
    if not value:
        success = False
        flash("Value is mandatory", "error")

    req = task.get_requirement(req_id)
    if not req:
        flash(f"Requirement {req_id} does not exists", "error")
        return False

    res_id = request.args.get("res_id")
    if not check_user_input_resolution(task, req, res_id):
        success = False

    if not success:
        return False

    res = req["resolution"][res_id]
    db = res["db"]
    key = res["key"]

    db_tools.set_value(task, req, [db, key, value])
    flash("Value successfully set", "notice")

    return True

def render_dep_list(task, dep_list, next_tree_id, breadcrumb):
    nodes_nr = 0
    method = dep_list[0]
    if method not in ["each", "any"]:
        raise InvalidConfiguration("Unknown method", method)
    class_html = f"dep dep_{method}"

    dependencies = dep_list[1:]
    dep_html = ""
    dep_status = []
    for dep in dependencies:
        single_html, single_status, single_nodes_nr = (
            render_dependencies(task, dep, next_tree_id, breadcrumb) )
        dep_html = dep_html + single_html
        dep_status.append(single_status)
        next_tree_id += single_nodes_nr
        nodes_nr += single_nodes_nr

    if method == "each":
        if False in dep_status:
            dep_list_fulfilled = False
        else:
            dep_list_fulfilled = True
    else:                       # Any
        if True in dep_status:
            dep_list_fulfilled = True
        else:
            dep_list_fulfilled = False

    if dep_list_fulfilled:
        fieldset_status_html = "req_fulfilled"
    else:
        fieldset_status_html = "req_not_fulfilled"

    # html = f"<div class='{class_html}'>{dep_html}</div>"
    html = f"""
<fieldset class='{fieldset_status_html}'>
  <legend>{method}</legend>
  {dep_html}
</fieldset>"""

    return html, dep_list_fulfilled, nodes_nr

def render_dependencies(task, dep_arg, next_tree_id, breadcrumb):
    dependencies_fulfilled = False
    nodes_nr = 0

    if not dep_arg:
        html = ""
        fulfilled = True

    elif type(dep_arg) is str:
        dep_html, fulfilled, nodes_nr = render_requirement(task, dep_arg,
                                                           next_tree_id,
                                                           breadcrumb,
                                                           False)
        html = f"<div class='dep'>{dep_html}</div>"

    elif type(dep_arg) is list:
        html, fulfilled, nodes_nr = render_dep_list(task, dep_arg,
                                                    next_tree_id, breadcrumb)

    return html, fulfilled, nodes_nr

def get_auto_res_form(req_id, res_id, res_label, enable_button, prev_arg):
    disable = "" if enable_button else "disabled=''"

    html = (
        "<form>"
        "  <input type='hidden' name='prev' value='{prev_arg}'/>"
        "  <input type='hidden' name='req_id' value='{req_id}'/>"
        "  <input type='hidden' name='res_id' value='{res_id}'/>"
        "  <input type='submit' {block} name='run_auto_res' value='{label}'/>"
        "</form>".format(prev_arg=prev_arg, req_id=req_id,
                         res_id=res_id, block=disable, label=res_label))
    return html

def check_only_manual_resolutions(req):
    resolutions = req.get("resolution")
    if not resolutions:
        return True

    for res_id in resolutions:
        res = resolutions[res_id]
        if res["method"] != "ui.manual":
            return False

    return True

def render_quick_auto_res(req, dep_status, prev_arg):
    html = ""

    resolutions = req.get("resolution")
    if not resolutions:
        return html

    for res_id in resolutions:
        res = resolutions[res_id]
        if res.get("method") == "automatic":
            if res.get("quick-access") == True:
                enable_button = False
                if dep_status == True or res.get("safe") == True:
                    enable_button = True

                html += get_auto_res_form(req["id"], res_id, res["label"],
                                          enable_button, prev_arg)

    return html

def render_requirement(task, req_id, next_tree_id, breadcrumb, first_call):
    req = task.get_requirement(req_id)
    req_label = req['label']
    do_collapse = (req.get('collapse') == True) and (not first_call)
    dep_html = ""
    classes_html = "env_req"
    quick_res_html = ""
    nodes_nr = 0
    next_corridor = breadcrumb.get_next_corridor(next_tree_id)

    if do_collapse:
        req_url = url_for('env.page_env_tree',
                          req_id=req_id,
                          prev=next_corridor)
        classes_html = append_class(classes_html, "req_collapsed")

    else:
        req_url = url_for('env.page_auto_res',
                          req_id=req_id,
                          prev=next_corridor)

        # Display the quick resolutions only if the requirement is not
        # collapsed
        dep_status = task.check_requirement_dependencies(req)
        quick_res_html = render_quick_auto_res(req, dep_status, next_corridor)

    req_fulfilled = task.check_requirement_status(req)

    if req_fulfilled:
        classes_html = append_class(classes_html, "req_fulfilled")
    else:
        classes_html = append_class(classes_html, "req_not_fulfilled")

    if check_only_manual_resolutions(req) == True:
        classes_html = append_class(classes_html, "req_dead_end")

    if not do_collapse:
        dep_html, _, nodes_nr = render_dependencies(task,
                                                    req.get('dependencies'),
                                                    next_tree_id + 1,
                                                    breadcrumb)

    nodes_nr += 1               # Count the current node

    html = f"""
<div id=tree-id-{next_tree_id} class='{classes_html}'>
  <a href='{req_url}'>{req_label}</a>
  {quick_res_html}
  {dep_html}
</div>"""

    return html, req_fulfilled, nodes_nr

def env_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if not session["env_name"]:
            select_env_url = url_for('select_env.page_select_env')
            link = f"<a href={select_env_url}>select one first</a>"
            flash(Markup(f"No environment selected, {link}"), "warning")

            return redirect(url_for('home.page_home'))

        return view(**kwargs)

    return wrapped_view

@blueprint.route('/tree', methods=["GET"])
@env_required
def page_env_tree():
    workspace = get_workspace()
    env = workspace.get_environment(session["env_name"])
    task = Task(workspace, env)

    if request.args.get("req_id"):
        target = request.args.get("req_id")
    else:
        target = task.get_target_requirement_name()

    breadcrumb = Breadcrumb(request.args.get("prev"))
    breadcrumb.prepare_next_corridor(target)

    # Case where the user used a quick automatic resolution
    if request.args.get("run_auto_res"):
        tree_anchor = get_tree_anchor(breadcrumb.prev_tree_id)
        run_auto_res(task, target)
        return redirect(url_for("env.page_env_tree",
                                _anchor=tree_anchor,
                                req_id=breadcrumb.prev_req_id,
                                prev=breadcrumb.prev_str))

    tree_html, _, _ = render_requirement(task, target, 0, breadcrumb, True)

    return render_template('env_tree.html',
                           tree_html=Markup(tree_html), breadcrumb=breadcrumb)

@blueprint.route('/auto-res/<req_id>', methods=["GET"])
@env_required
def page_auto_res(req_id=None):
    workspace = get_workspace()
    env = workspace.get_environment(session["env_name"])
    task = Task(workspace, env)
    breadcrumb = Breadcrumb(request.args.get("prev"))

    if request.method == "GET":

        do_redirect = False

        if request.args.get("run_auto_res"):
            run_auto_res(task, req_id)
            do_redirect = True

        if request.args.get("set_value"):
            set_value_from_user(task, req_id)
            do_redirect = True

        if request.args.get("user_select_submit"):
            set_value_from_user(task, req_id)
            do_redirect = True

        if do_redirect:
            return redirect(url_for("env.page_auto_res", req_id=req_id,
                                    prev=breadcrumb.orig_str))

    try:
        req = task.get_requirement(req_id)
        return render_template('env_auto_res.html', task=task, req=req,
                               breadcrumb=breadcrumb)
    except InvalidConfiguration:
        flash("Unknown requirement {}".format(req_id), "error")
        return redirect(url_for("env.page_env_tree"))
