from flask import Flask
from api import api
import logging, os


def create_app():
    app = Flask(__name__)
    app.secret_key = "this is the secret key"
    app.register_blueprint(api)
    file_handler = logging.FileHandler('app.log')
    os.chmod('app.log', 0o777)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', threaded=True)
