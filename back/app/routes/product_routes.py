from flask import Blueprint, request, jsonify
from werkzeug.exceptions import BadRequest, NotFound
import json

from app.libs.redis import insert_queue
from app.services.logger import LoggerService

from app.routes.models import ProductModel

from app.models.repository.product_repository import (
    find_product_by_id,
    find_all_products,
    delete_product,
    create_product_job,
    update_product_job,
)

products_routes = Blueprint(
    "products", 
    __name__, 
    url_prefix="/products"
)
logger = LoggerService()


@products_routes.get("")
def list_products():
    try:
        page = request.args.get("page", default=1, type=int)
        limit = request.args.get("limit", default=100, type=int)

        # alores mínimos válidos
        if page < 1:
            page = 1

        if limit < 1:
            limit = 100

        products = find_all_products(page, limit)

        return jsonify({
            "success": True,
            "data": products
        }), 200

    except Exception as e:
        logger.log(
            route=str(request.url),
            method=request.method,
            message=f"Product Get All - Error sending to queue: {e}",
            level="error"
        )
        
        raise e
    
@products_routes.post("")
def create_product():
    try:
        product = ProductModel.model_validate(request.json)
        
        message = {
            "data": {
                "name": product.name,
                "mark": product.mark,
                "value": product.value
            }
        }

        insert_queue(create_product_job, json.dumps(message))

        logger.log(
            route=str(request.url),
            method=request.method,
            message=f"Product - Sent to queue: {product.name}",
        )

        return jsonify({
            "success": True,
            "message": "Produto enviado para processamento"
        }), 202

    except Exception as e:
        logger.log(
            route=str(request.url),
            method=request.method,
            message=f"Product Create - Error sending to queue: {e}",
            level="error"
        )
        
        raise e
    
@products_routes.put("/<int:product_id>")
def update_product(product_id):
    try:
        product = ProductModel.model_validate(request.json)

        message = {
            "data": {
                "id": product_id,
                "name": product.name,
                "mark": product.mark,
                "value": product.value,
            }
        }

        insert_queue(update_product_job, json.dumps(message))

        return jsonify({
            "success": True,
            "message": "Atualização enviada para processamento"
        }), 202

    except Exception as e:
        logger.log(
            route=str(request.url),
            method=request.method,
            message=f"Product Update - Error sending to queue: {e}",
            level="error"
        )
        
        raise e
    
@products_routes.delete("/<int:product_id>")
def remove_product(product_id):
    try:
        product = delete_product(product_id)

        if not product:
            raise NotFound("Produto não encontrado")

        return jsonify({
            "success": True,
            "message": "Produto removido com sucesso"
        }), 200

    except Exception as e:
        logger.log(
            route=str(request.url),
            method=request.method,
            message=f"Product Delete - Error sending to queue: {e}",
            level="error"
        )
         
        raise e