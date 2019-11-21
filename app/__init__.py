from flask import Flask
from app.models.base import db
from flask_login import LoginManager
from flask_cors import CORS

login_manager = LoginManager()


def create_app():
    app = Flask(__name__,
            static_folder="../dist/static",
            template_folder="../dist")
    # app = Flask(__name__)
    CORS(app, supports_credentials=True, resources=r'/*')
    app.config.from_object('app.config')

    db.init_app(app)
    login_manager.init_app(app)

    register_blueprint(app)

    with app.app_context():

        db.create_all(app=app)

    return app


def register_blueprint(app):
    from app.web.wx_mini import web
    app.register_blueprint(web)
