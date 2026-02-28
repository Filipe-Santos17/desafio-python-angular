from flask import Flask

from global_error import global_error_handler
from app.routes import auth_routes, products_routes
from app.envs import envs

app = Flask(__name__)
global_error_handler(app)

app.register_blueprint(auth_routes)
app.register_blueprint(products_routes)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=envs["ENVIRONMENT"] == "dev")