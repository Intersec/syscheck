import functools

from flask import Blueprint, render_template

blueprint = Blueprint('env', __name__, url_prefix='/env')

@blueprint.route('/tree', methods=["GET"])
def page_env_tree():
    return render_template('env_tree.html')
