import os
import logging

from {{cookiecutter.module_name}} import load_dotenv, create_app

load_dotenv()

app = create_app()

if __name__ == "__main__":
    log: logging.Logger = app.logger
    log.setLevel(logging.DEBUG)
    app.run(host=os.getenv("APP_HOST"), port=os.getenv("APP_PORT"), debug=True)
