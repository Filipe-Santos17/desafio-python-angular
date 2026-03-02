import logging
import json
from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from werkzeug.exceptions import (
    BadRequest,
    InternalServerError,
    HTTPException,
)

from app.auth import jwt_required
from app.libs.redis import insert_queue
from app.routes.models import ProductModel
from app.models.repository.product_repository import (
    find_all_products,
    delete_product,
    create_product_job,
    update_product_job,
)

products_routes = Namespace(
    "products",
    description="Operações de gerenciamento de produtos"
)

logger = logging.getLogger(__name__)

# Models
product_request_model = products_routes.model("ProductRequest", {
    "name": fields.String(required=True, example="Notebook"),
    "mark": fields.String(required=True, example="Dell"),
    "value": fields.Float(required=True, example=4500.00)
})

product_response_model = products_routes.model("ProductResponse", {
    "id": fields.Integer(example=1),
    "name": fields.String(example="Notebook"),
    "mark": fields.String(example="Dell"),
    "value": fields.Float(example=4500.00),
})

list_response_model = products_routes.model("ListProductsResponse", {
    "success": fields.Boolean(example=True),
    "data": fields.List(fields.Nested(product_response_model))
})

default_response_model = products_routes.model("DefaultResponse", {
    "success": fields.Boolean(example=True),
    "message": fields.String(example="Operação realizada com sucesso")
})

# Rotas
@products_routes.route("")
class ProductList(Resource):
    @products_routes.doc(security="Bearer")
    @products_routes.param("page", "Número da página", type=int)
    @products_routes.param("limit", "Quantidade de registros por página", type=int)
    @products_routes.response(200, "Lista retornada com sucesso", list_response_model)
    @products_routes.response(401, "Não autorizado")
    @jwt_required()
    def get(self):
        try:
            page = request.args.get("page", default=1, type=int)
            limit = request.args.get("limit", default=100, type=int)

            page = max(page, 1)
            limit = max(limit, 1)

            products = find_all_products(page, limit)

            return {
                "success": True,
                "data": products
            }, 200

        except HTTPException as e:
            raise e
        except Exception as e:
            logger.error(f"Product Get All - Error: {e}", exc_info=True)

            raise InternalServerError("Falha do servidor ao selecionar produtos")

    @products_routes.doc(security="Bearer")
    @products_routes.expect(product_request_model)
    @products_routes.response(202, "Produto enviado para processamento", default_response_model)
    @products_routes.response(400, "Erro de validação")
    @products_routes.response(401, "Não autorizado")
    @jwt_required()
    def post(self):
        try:
            product = ProductModel.safe_validate(request.json)

            if not product:
                raise BadRequest("Dados inválidos/incompletos")

            message = {
                "operation": "create",
                "data": {
                    "name": product.name,
                    "mark": product.mark,
                    "value": product.value
                }
            }

            insert_queue(create_product_job, json.dumps(message))

            logger.info(f"Create Product - Sent to queue: {product.name}")

            return {
                "success": True,
                "message": "Produto enviado para processamento"
            }, 202

        except HTTPException as e:
            raise e
        except Exception as e:
            logger.error(f"Create Product - Error: {e}", exc_info=True)

            raise InternalServerError("Falha do servidor ao postar produto")


@products_routes.route("/<int:product_id>")
class ProductDetail(Resource):
    @products_routes.doc(security="Bearer")
    @products_routes.expect(product_request_model)
    @products_routes.response(202, "Atualização enviada para processamento", default_response_model)
    @products_routes.response(401, "Não autorizado")
    @jwt_required()
    def put(self, product_id: int):
        try:
            product = ProductModel.safe_validate(request.json)

            if not product:
                raise BadRequest("Dados inválidos/incompletos")

            message = {
                "operation": "update",
                "data": {
                    "id": product_id,
                    "name": product.name,
                    "mark": product.mark,
                    "value": product.value,
                }
            }

            insert_queue(update_product_job, json.dumps(message))

            logger.info(f"Update Product - Sent to queue: {product_id}")

            return {
                "success": True,
                "message": "Atualização enviada para processamento"
            }, 202

        except HTTPException as e:
            raise e
        except Exception as e:
            logger.error(f"Update Product - Error: {e}", exc_info=True)

            raise InternalServerError("Falha do servidor ao atualizar produto")

    @products_routes.doc(security="Bearer")
    @products_routes.response(200, "Produto enviado para exclusão", default_response_model)
    @products_routes.response(401, "Não autorizado")
    @jwt_required()
    def delete(self, product_id: int):
        try:
            message = {
                "operation": "delete",
                "data": {
                    "id": product_id,
                }
            }

            insert_queue(delete_product, json.dumps(message))

            logger.info(f"Delete Product - Sent to queue: {product_id}")

            return {
                "success": True,
                "message": "Remoção enviada para processamento"
            }, 200
        
        except HTTPException as e:
            raise e
        except Exception as e:
            logger.error(f"Delete Product - Error: {e}", exc_info=True)
            
            raise InternalServerError("Falha do servidor ao deletar produto")