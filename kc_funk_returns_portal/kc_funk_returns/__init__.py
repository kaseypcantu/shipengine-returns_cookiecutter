from dotenv import load_dotenv
from flask import Flask
from flask_mail import Mail

from kc_funk_returns.se_client import ShipEngine
from kc_funk_returns.config import Config

load_dotenv()

mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    app.app_context().push()

    mail.init_app(app)

    from kc_funk_returns.main_routes.routes import main
    from kc_funk_returns.api.routes import api
    from kc_funk_returns.error_routes.handlers import errors

    app.register_blueprint(main)
    app.register_blueprint(api)
    app.register_blueprint(errors)

    return app
