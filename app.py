"""Main file for python server."""

from server.app_factory import create_app, create_api
from server.api import api_config
from server.logger import log

# Create the flask app
app, db = create_app()

with app.app_context():
  api_manager = create_api(app, db, api_config)

if __name__ == "__main__":
    app.run(debug=True)
