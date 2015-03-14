import json
from flask import render_template, request, Response

from server.mod_auth.auth import login
from flask_login import current_user


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
