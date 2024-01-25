import functools

from flask import (Blueprint,
                   render_template,
                   session,
                   flash,
                   url_for,
                   Markup,
                   redirect)

blueprint = Blueprint('env', __name__, url_prefix='/env')

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
    return render_template('env_tree.html')
