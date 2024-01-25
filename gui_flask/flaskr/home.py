import functools

from flask import Blueprint, render_template
# flash, g, redirect, render_template, request, session, url_for

blueprint = Blueprint('home', __name__, url_prefix='/home')

@blueprint.route('/', methods=["GET"])
def page_home():
    return render_template('home.html')
