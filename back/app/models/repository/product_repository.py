from sqlalchemy import text
import json

from app.models.database import DBConnection
from app.models.entities import Product

def find_all_products(page: int = 1, limit_per_page: int = 100):
    try:
        with DBConnection() as db:
            result = db.execute(
                text("""
                    SELECT * FROM products
                    ORDER BY id ASC
                    LIMIT :limit OFFSET :offset
                """),
                {"limit": limit_per_page, "offset": (page - 1) * limit_per_page}
            ).fetchall()

            products = []

            for row in result:
                data = dict(**row._mapping)

                if data.get("created_at"):
                    data["created_at"] = data["created_at"].isoformat()

                if data.get("updated_at"):
                    data["updated_at"] = data["updated_at"].isoformat()

                products.append(data)

            return products
    except Exception as e:
        raise e


def find_product_by_id(product_id: int):
    try:
        with DBConnection() as db:
            result = db.execute(
                text("SELECT * FROM products WHERE id = :id"),
                {"id": product_id}
            ).first()

            if not result:
                return None

            return Product(**result._mapping)
    except Exception as e:
        raise e


def delete_product(raw_message: str):
    try:
        message = json.loads(raw_message)

        data = message["data"]
        
        with DBConnection() as db:
            result = db.execute(
                text("DELETE FROM products WHERE id = :id"),
                {"id": data["id"]}
            )

            return result.rowcount
    except Exception as e:
        raise e
    

def create_product_job(raw_message: str):
    try:
        message = json.loads(raw_message)

        data = message["data"]
        
        with DBConnection() as db:
            prod = Product(
                name=data['name'],
                mark=data['mark'],
                value=data['value'],
            )

            db.add(prod)
    except Exception as e:
        raise e

def update_product_job(raw_message: str):
    try:
        message = json.loads(raw_message)

        data = message["data"]
    
        with DBConnection() as db:
            result = db.execute(
                text("""
                    UPDATE products
                    SET name = :name, mark = :mark, value = :value
                    WHERE id = :id
                """),
                data
            )
        
        return result.rowcount
    except Exception as e:
        raise e
        
