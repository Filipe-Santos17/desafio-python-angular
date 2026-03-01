import logging
from flask import Blueprint, request, jsonify
import json

from app.auth import jwt_required
from app.libs.redis import insert_queue
from app.routes.models import ProductModel
from app.models.repository.product_repository import (
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

logger = logging.getLogger(__name__)


@products_routes.get("")
@jwt_required()
def list_products():
    try:
        page = request.args.get("page", default=1, type=int)
        limit = request.args.get("limit", default=100, type=int)

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
        logger.error(
            f"Product Get All - Error: {e}",
            exc_info=True
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

        logger.info(
            f"Create Product - Sent to queue: {product.name}"
        )

        return jsonify({
            "success": True,
            "message": "Produto enviado para processamento"
        }), 202

    except Exception as e:
        logger.error(
            f"Create Product - Error: {e}",
            exc_info=True
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

        logger.info(
            f"Update Product - Sent to queue: {product_id}, {product.name}"
        )

        return jsonify({
            "success": True,
            "message": "Atualização enviada para processamento"
        }), 202

    except Exception as e:
        logger.error(
            f"Update Product - Error: {e}",
            exc_info=True
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

        logger.info(
            f"Delete Product - Sent to queue: {product_id}"
        )

        return jsonify({
            "success": True,
            "message": "Atualização enviada para processamento"
        }), 200

    except Exception as e:
        logger.error(
            f"Delete Product - Error: {e}",
            exc_info=True
        )
        raise e