import json
from flask import render_template, request, Response

from server.mod_auth.auth import login
from flask_login import current_user, login_required
from flask_restless import ProcessingException
from server.models import db, Event


def owner_or_admin_required(instance_id: int, *args, **kwargs):
    """Ensure only an event owner or an admin can update an event."""
    if (
        not current_user.owns_event_with_id(instance_id) and
        not current_user.is_admin
    ):
        raise ProcessingException(
            'Only event owners or admins can update this event')


def define_routes(app):
    @app.route('/', methods=['GET'])
    def index():
        return render_template('index.html')

    @app.route('/user/login', methods=['POST'])
    def route_login():
        return login(request)

    # Serve Static Assets
    # TODO: Do this with apache or nginx
    @app.route('/static/<path:file_path>.<extension>', methods=['GET'])
    def static_proxy(file_path, extension):
        file_path = file_path.rstrip('/') + "." + extension
        app.logger.info('File Path: %s' % file_path)
        return app.send_static_file(file_path)

    @app.route('/user/isLoggedIn', methods=['GET'])
    def is_logged_in():
        data = {
            'isLoggedIn': current_user.is_authenticated()
        }
        resp = Response(
            json.dumps(data), status=200, mimetype='application/json')

        return resp

    @app.route('/event/<event_id>', methods=['DELETE'])
    @login_required
    def delete_event(event_id):
        owner_or_admin_required(event_id)
        event = Event.query.filter_by(id=event_id).first()
        db.session.delete(event)
        db.session.commit()
        return Response("", status=204, mimetype='application/json')
