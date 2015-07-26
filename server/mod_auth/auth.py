"""This module contains functions for handling user authentication."""
import flask
import json
from flask_login import login_user
from server.models import User
from server.login_manager import login_manager


def tmp_auth(request: flask.Request):
    auth = request.authorization
    if not auth:
        return "NO AUTH"
    return User.query.filter_by(
        username=auth.username,
        password=auth.password
    ).first()


@login_manager.user_loader
def load_user(user_id: int) -> User:
    """Return a user from the database based on their id.

    :param user_id: a users unique id
    :return: User object with corresponding id, or none if user does not exist
    """
    return User.query.filter_by(id=user_id).first()


def handle_basic_auth(request: flask.Request) -> User:
    """Verify a request using BASIC auth.

    :param request: flask request object
    :return: User object corresponding to login information, or none if
    user does not exist
    """
    auth = request.authorization
    if not auth:
        return None
    return User.query.filter_by(
        username=auth.username,
        password=auth.password
    ).first()


def login(request: flask.Request) -> flask.Response:
    """Handle a login request from a user.

    :param request: incoming request object
    :return: flask response object
    """
    user = handle_basic_auth(request)

    if user:
        login_user(user, remember=True)
        body = json.dumps({})
        return flask.Response(body, status=200, mimetype='application/json')
    return flask.Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})
