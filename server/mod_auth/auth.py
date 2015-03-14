import flask
import json
from flask_login import login_user
from server.models import User
from server.login_manager import login_manager


@login_manager.user_loader
def load_user(user_id: int) -> User:
    """Returns a user from the database based on their id

    :param user_id: a users unique id
    :return: User object with corresponding id, or none if user does not exist
    """
    return User.query.filter_by(id=user_id).first()


def handle_basic_auth(request: flask.Request) -> User:
    """Verifies a request using BASIC auth

    :param request: flask request object
    :return: User object corresponding to login information, or none if user does not exist
    """
    auth = request.authorization
    log.log(logging.INFO, request.headers)
    log.log(logging.INFO, auth)
    if not auth:
        return None
    return User.query.filter_by(
        username=auth.username,
        password=auth.password
    ).first()


def login(request: flask.Request) -> flask.Response:
    """Handle a login request from a user

    :param request: incoming request object
    :return: flask response object
    """

    user = handle_basic_auth(request)
    log.log(logging.INFO, user)

    if user:
        login_user(user, remember=True)
        return flask.Response(json.dumps({}), status=200, mimetype='application/json')
    return flask.Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})
