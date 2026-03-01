from flask.testing import FlaskClient
from types import SimpleNamespace

from api import api

client: FlaskClient = api.test_client()


# LOGIN - SUCCESS
def test_e2e_login_success(mocker):
    fake_user = SimpleNamespace(
        id=1,
        email="filipe@teste.com",
        password="hashed123",
        name="Filipe",
    )

    mocker.patch("app.routes.auth_routes.find_user_by_email", return_value=fake_user)
    mocker.patch("app.routes.auth_routes.check_password", return_value=True)
    mocker.patch(
        "app.routes.auth_routes.generate_random_hash", return_value="session123"
    )
    mocker.patch(
        "app.routes.auth_routes.create_token_for_login_user",
        return_value=("access_token", "refresh_token"),
    )
    mocker.patch(
        "app.routes.auth_routes.clear_user", return_value={"email": fake_user.email}
    )

    resp = client.post(
        "/api/auth/login", json={"email": fake_user.email, "password": fake_user.password}
    )

    data = resp.get_json()

    assert resp.status_code == 200
    assert data["success"] is True
    assert data["access_token"] == "access_token"
    assert data["user"]["email"] == fake_user.email


# LOGIN - USER NOT FOUND
def test_e2e_login_user_not_found(mocker):
    mocker.patch("app.routes.auth_routes.find_user_by_email", return_value=None)

    resp = client.post("/api/auth/login", json={"email": "x@x.com", "password": "12345678"})

    data = resp.get_json()

    assert resp.status_code == 400
    assert data["error"]["message"] == "Email ou senha inválidos"


# LOGIN - WRONG PASSWORD
def test_e2e_login_wrong_password(mocker):
    fake_user = mocker.Mock()
    fake_user.password = "hashed"

    mocker.patch("app.routes.auth_routes.find_user_by_email", return_value=fake_user)
    mocker.patch("app.routes.auth_routes.check_password", return_value=False)

    resp = client.post(
        "/api/auth/login", json={"email": "x@x.com", "password": "wrong1234"}
    )

    data = resp.get_json()

    assert resp.status_code == 400
    assert data["error"]["message"] == "Email ou senha inválidos"


# REGISTER - SUCCESS
def test_e2e_register_success(mocker):
    mocker.patch("app.routes.auth_routes.find_user_by_email", return_value=None)
    mocker.patch("app.routes.auth_routes.hash_password", return_value="hashed")
    mocker.patch("app.routes.auth_routes.insert_user")

    resp = client.post(
        "/api/auth/register",
        json={"email": "novo@teste.com", "name": "Novo", "password": "senha1123"},
    )

    data = resp.get_json()

    assert resp.status_code == 201
    assert data["success"] is True
    assert data["msg"] == "Usuário criado"


# REGISTER - USER EXISTS
def test_e2e_register_user_exists(mocker):
    fake_user = mocker.Mock()

    mocker.patch("app.routes.auth_routes.find_user_by_email", return_value=fake_user)

    resp = client.post(
        "/api/auth/register",
        json={"email": "existente@teste.com", "name": "User", "password": "senha1123"},
    )

    data = resp.get_json()

    assert resp.status_code == 400
    assert data["error"]["message"] == "Usuário existente"


# LOGOFF - success
def test_e2e_logoff_success(mocker):
    mocker.patch("app.routes.auth_routes.remove_token")

    # mock jwt_required para bypass
    mocker.patch("app.routes.auth_routes.jwt_required", lambda: lambda f: f)

    resp = client.post("/api/auth/logoff")

    assert resp.status_code == 200
