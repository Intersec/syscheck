import functools

from flask import Blueprint, render_template

blueprint = Blueprint('db_tools', __name__, url_prefix='/db-tools')

@blueprint.route('/', methods=["GET"])
def page_db_tools():
    return render_template('db_tools.html')
