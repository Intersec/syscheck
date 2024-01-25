import functools

from flask import (Blueprint,
                   render_template,
                   session,
                   flash,
                   url_for,
                   Markup,
                   redirect)
from task import Task, InvalidConfiguration
from workspace import get_workspace

blueprint = Blueprint('env', __name__, url_prefix='/env')

def render_dep_list(task, dep_list):
    method = dep_list[0]
    if method not in ["each", "any"]:
        raise InvalidConfiguration("Unknown method", method)
    class_html = f"dep dep_{method}"

    dependencies = dep_list[1:]
    dep_html = ""
    dep_status = []
    for dep in dependencies:
        # dep_html = dep_html + render_requirement(task, dep)
        single_html, single_status = render_dependencies(task, dep)
        dep_html = dep_html + single_html
        dep_status.append(single_status)

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

    return html, dep_list_fulfilled

def render_dependencies(task, dep_arg):
    dependencies_fulfilled = False

    if not dep_arg:
        html = ""
        fulfilled = True

    elif type(dep_arg) is str:
        dep_html, fulfilled = render_requirement(task, dep_arg)
        html = f"<div class='dep'>{dep_html}</div>"

    elif type(dep_arg) is list:
        html, fulfilled = render_dep_list(task, dep_arg)

    return html, fulfilled

def render_requirement(task, req_id):
    req = task.get_requirement(req_id)
    req_label = req['label']

    req_fulfilled = task.check_requirement_status(req)

    if req_fulfilled:
        req_status_html = "req_fulfilled"
    else:
        req_status_html = "req_not_fulfilled"

    dep_html, _ = render_dependencies(task, req.get('dependencies'))

    html = f"""
<div class='env_req {req_status_html}'>
  <label>{req_label}</label>
  {dep_html}
</div>"""

    return html, req_fulfilled

def env_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if not session["env_name"]:
            select_env_url = url_for('select_env.page_select_env')
            link = "<a href={select_env_url}>select one first</a>"
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
    task_target = task.get_target_requirement_name()
    tree_html, _ = render_requirement(task, task_target)

    return render_template('env_tree.html', tree_html=Markup(tree_html))
