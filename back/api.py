from flask import Flask
from flask_restx import Api
from werkzeug.middleware.proxy_fix import ProxyFix

from global_error import global_error_handler
from app.routes import auth_routes, products_routes
from app.envs import envs
from app.services.logger import setup_logging

api = Flask(__name__)

api.config["PREFERRED_URL_SCHEME"] = "http"

# Corrige problemas de proxy / docker / https
api.wsgi_app = ProxyFix(api.wsgi_app, x_proto=1, x_host=1)

authorizations = {
    "Bearer": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization"
    }
}

# Swagger
rest_api = Api(
    api,
    version="1.0",
    title="Product API",
    description="API para gerenciamento de produtos",
    doc="/api/docs",
    prefix="/api",
    authorizations=authorizations,
    security="Bearer",
    serve_challenge_on_401=True,
)

global_error_handler(rest_api)

setup_logging()

# Registra namespaces / rotas
rest_api.add_namespace(auth_routes)
rest_api.add_namespace(products_routes)

if __name__ == '__main__':
    api.run(
        host="0.0.0.0",
        port=5000,
        debug=envs["ENVIRONMENT"] == "dev"
    )