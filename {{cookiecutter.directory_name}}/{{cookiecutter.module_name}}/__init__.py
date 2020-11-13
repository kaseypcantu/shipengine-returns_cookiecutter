from dotenv import load_dotenv
from flask import Flask
from flask_mail import Mail

from {{cookiecutter.module_name}}.se_client import ShipEngine
from {{cookiecutter.module_name}}.config import Config

load_dotenv()

mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    app.app_context().push()

    mail.init_app(app)

    from {{cookiecutter.module_name}}.main_routes.routes import main
    from {{cookiecutter.module_name}}.api.routes import api
    from {{cookiecutter.module_name}}.error_routes.handlers import errors

    app.register_blueprint(main)
    app.register_blueprint(api)
    app.register_blueprint(errors)

    return app
