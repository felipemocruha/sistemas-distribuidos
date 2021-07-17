from flask import Flask
from flask_cors import CORS

from service.views import api
from service.config import SECRET_KEY


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.register_blueprint(api, url_prefix='/api/v1')

    return app
