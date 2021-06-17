from flask import Flask
from service.handlers import api


def create_app():
    app = Flask(__name__)
    app.register_blueprint(api, url_prefix='/api/v1')

    return app
