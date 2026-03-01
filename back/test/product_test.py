from flask.testing import FlaskClient

from api import api

api.config["TESTING"] = True

client: FlaskClient = api.test_client()

# LIST PRODUCTS - SUCCESS
def test_e2e_list_products_success(mocker):
    fake_products = [
        {"id": 1, "name": "Produto 1"},
        {"id": 2, "name": "Produto 2"},
    ]

    mocker.patch(
        "app.routes.product_routes.find_all_products",
        return_value=fake_products,
    )

    # bypass jwt
    mocker.patch("app.routes.product_routes.jwt_required", lambda: lambda f: f)

    resp = client.get("/api/products?page=1&limit=10")

    data = resp.get_json()

    assert resp.status_code == 200
    assert data["success"] is True
    assert data["data"] == fake_products


# CREATE PRODUCT - SUCCESS
def test_e2e_create_product_success(mocker):
    mocker.patch("app.routes.product_routes.insert_queue")
    mocker.patch("app.routes.product_routes.jwt_required", lambda: lambda f: f)

    resp = client.post(
        "/api/products",
        json={
            "name": "Produto Novo",
            "mark": "Marca X",
            "value": 100,
        },
    )

    data = resp.get_json()

    assert resp.status_code == 202
    assert data["success"] is True
    assert data["message"] == "Produto enviado para processamento"


# UPDATE PRODUCT - SUCCESS
def test_e2e_update_product_success(mocker):
    mocker.patch("app.routes.product_routes.insert_queue")
    mocker.patch("app.routes.product_routes.jwt_required", lambda: lambda f: f)

    resp = client.put(
        "/api/products/1",
        json={
            "name": "Produto Atualizado",
            "mark": "Marca Y",
            "value": 200,
        },
    )

    data = resp.get_json()
    
    assert resp.status_code == 202
    assert data["success"] is True
    assert data["message"] == "Atualização enviada para processamento"


# DELETE PRODUCT - SUCCESS
def test_e2e_delete_product_success(mocker):
    mocker.patch("app.routes.product_routes.insert_queue")
    mocker.patch("app.routes.product_routes.jwt_required", lambda: lambda f: f)

    resp = client.delete("/api/products/1")

    data = resp.get_json()

    assert resp.status_code == 200
    assert data["success"] is True
    assert data["message"] == "Remoção enviada para processamento"


# LIST PRODUCTS - FAIL WITHOUT TOKEN
def test_e2e_list_products_without_token():
    api.config["TESTING"] = False
    
    resp = client.get("/api/products")
    assert resp.status_code == 401