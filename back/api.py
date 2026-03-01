from flask import Flask

from global_error import global_error_handler
from app.routes import auth_routes, products_routes
from app.envs import envs
from app.services.logger import setup_logging

api = Flask(__name__)
global_error_handler(api)

setup_logging()

api.register_blueprint(auth_routes)
api.register_blueprint(products_routes)

if __name__ == '__main__':
    api.run(host="0.0.0.0", port=5000, debug=envs["ENVIRONMENT"] == "dev")