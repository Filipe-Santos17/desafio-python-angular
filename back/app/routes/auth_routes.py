import logging
from flask import request, make_response, jsonify
from flask_restx import Namespace, Resource, fields
from werkzeug.exceptions import (
    BadRequest,
    InternalServerError,
    HTTPException,
)

from app.auth import (
    create_token_for_login_user,
    add_token_to_response,
    remove_token,
    jwt_required,
)

from app.libs.crypto import check_password, hash_password
from app.models.repository import find_user_by_email, insert_user
from app.routes.models import LoginSchema, RegisterUser
from app.utils.random import generate_random_hash
from app.utils.clear_user import clear_user

auth_routes = Namespace(
    "auth",
    description="Operações de autenticação"
)

logger = logging.getLogger(__name__)

# Models
login_model = auth_routes.model("LoginRequest", {
    "email": fields.String(required=True, example="user@email.com"),
    "password": fields.String(required=True, example="123456")
})

register_model = auth_routes.model("RegisterRequest", {
    "name": fields.String(required=True, example="Filipe"),
    "email": fields.String(required=True, example="user@email.com"),
    "password": fields.String(required=True, example="123456")
})

user_response_model = auth_routes.model("UserResponse", {
    "id": fields.Integer(example=1),
    "name": fields.String(example="Filipe"),
    "email": fields.String(example="user@email.com")
})

login_response_model = auth_routes.model("LoginResponse", {
    "user": fields.Nested(user_response_model),
    "access_token": fields.String,
    "success": fields.Boolean(example=True)
})

default_response_model = auth_routes.model("DefaultResponse", {
    "msg": fields.String,
    "success": fields.Boolean
})

# Rotas
@auth_routes.route("/login")
class Login(Resource):
    @auth_routes.expect(login_model)
    @auth_routes.response(200, "Login realizado com sucesso", login_response_model)
    @auth_routes.response(400, "Email ou senha inválidos")
    @auth_routes.response(500, "Erro interno do servidor")
    def post(self):
        try:
            login_user = LoginSchema.safe_validate(request.json)

            if not login_user:
                raise BadRequest("Dados inválidos/incompletos")

            email_user = login_user.email
            password_user = login_user.password

            user = find_user_by_email(email_user)

            if not user:
                raise BadRequest("Email ou senha inválidos")

            if not check_password(password_user, user.password):
                raise BadRequest("Email ou senha inválidos")

            random_code_session = generate_random_hash()
            token, refresh_token = create_token_for_login_user(
                user.id, random_code_session
            )

            user_clear = clear_user(user)

            resp = make_response(
                jsonify(
                    {
                        "user": user_clear,
                        "access_token": token,
                        "success": True,
                    }
                ),
                200,
            )

            add_token_to_response(resp, refresh_token)

            return resp

        except HTTPException as e:
            raise e
        except Exception as e:
            logger.error(str(e), exc_info=True)

            raise InternalServerError("Falha do servidor ao realizar login")

@auth_routes.route("/register")
class Register(Resource):
    @auth_routes.expect(register_model)
    @auth_routes.response(201, "Usuário criado com sucesso", default_response_model)
    @auth_routes.response(400, "Usuário já existente")
    @auth_routes.response(500, "Erro interno do servidor")
    def post(self):
        try:
            register_user = RegisterUser.safe_validate(request.json)

            if not register_user:
                raise BadRequest("Dados inválidos/incompletos")

            email_user = register_user.email

            if find_user_by_email(email_user):
                raise BadRequest("Usuário existente")

            password_hash = hash_password(register_user.password)

            insert_user(
                email=email_user,
                name=register_user.name,
                password=password_hash,
            )

            return {"msg": "Usuário criado", "success": True}, 201

        except HTTPException as e:
            raise e
        except Exception as e:
            logger.error(str(e), exc_info=True)

            raise InternalServerError("Falha ao realizar cadastro")

@auth_routes.route("/logoff")
class Logoff(Resource):
    @auth_routes.doc(security="Bearer")
    @auth_routes.response(200, "Logoff realizado com sucesso", default_response_model)
    @auth_routes.response(401, "Não autorizado")
    @auth_routes.response(500, "Erro interno do servidor")
    @jwt_required()
    def post(self):
        try:
            resp = make_response(
                jsonify({"msg": "Logoff concluido", "success": True}),
                200,
            )

            remove_token(resp)

            return resp

        except Exception as e:
            logger.error(str(e), exc_info=True)

            raise InternalServerError("Falha do servidor ao realizar logoff")