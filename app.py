from flask import Flask
from api import api
import logging, os


def create_app():
    app = Flask(__name__)
    app.secret_key = "this is the secret key"
    app.register_blueprint(api)
  #  cwd = os.getcwd()
  #  log_file = cwd + '/app.log'
  #    os.chmod(log_file, 0o777)
    file_handler = logging.FileHandler('/tmp/app.log')
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.ERROR)
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', threaded=True)
