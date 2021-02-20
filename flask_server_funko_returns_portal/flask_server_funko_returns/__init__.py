from dotenv import load_dotenv
from flask import Flask
from flask_mail import Mail

from flask_server_funko_returns.se_client import ShipEngine
from flask_server_funko_returns.config import Config

load_dotenv()

mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    app.app_context().push()

    mail.init_app(app)

    from flask_server_funko_returns.main_routes.routes import main
    from flask_server_funko_returns.api.routes import api
    from flask_server_funko_returns.error_routes.handlers import errors

    app.register_blueprint(main)
    app.register_blueprint(api)
    app.register_blueprint(errors)

    return app
