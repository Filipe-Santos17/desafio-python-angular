from flask import Blueprint, request, jsonify
from werkzeug.exceptions import BadRequest, NotFound
import json

from app.auth import jwt_required

from app.libs.redis import insert_queue

from app.services.logger import logger

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

@products_routes.get("")
@jwt_required()
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
@jwt_required()
def create_product():
    try:
        product = ProductModel.model_validate(request.json)
        
        message = {
            "operation": "create",
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
            message=f"Create Product - Sent to queue: {product.name}",
        )

        return jsonify({
            "success": True,
            "message": "Produto enviado para processamento"
        }), 202

    except Exception as e:
        logger.log(
            route=str(request.url),
            method=request.method,
            message=f"Create Product - Error sending to queue: {e}",
            level="error"
        )
        
        raise e
    
@products_routes.put("/<int:product_id>")
@jwt_required()
def update_product(product_id: int):
    try:
        product = ProductModel.model_validate(request.json)

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
        
        logger.log(
            route=str(request.url),
            method=request.method,
            message=f"Update Product - Sent to queue: {product_id}, {product.name}",
        )

        return jsonify({
            "success": True,
            "message": "Atualização enviada para processamento"
        }), 202

    except Exception as e:
        logger.log(
            route=str(request.url),
            method=request.method,
            message=f"Update Product - Error sending to queue: {e}",
            level="error"
        )
        
        raise e
    
@products_routes.delete("/<int:product_id>")
@jwt_required()
def remove_product(product_id: int):
    try:
        message = {
           "operation": "delete",
           "data": {
               "id": product_id,
           }
        }

        insert_queue(delete_product, json.dumps(message))
        
        logger.log(
            route=str(request.url),
            method=request.method,
            message=f"Delete Product - Sent to queue: {product_id}",
        )
        
        return jsonify({
            "success": True,
            "message": "Atualização enviada para processamento"
        }), 200

    except Exception as e:
        logger.log(
            route=str(request.url),
            method=request.method,
            message=f"Delete Product - Error sending to queue: {e}",
            level="error"
        )
         
        raise e