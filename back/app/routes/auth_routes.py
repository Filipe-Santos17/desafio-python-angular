from flask import request, make_response, Blueprint, jsonify
from werkzeug.exceptions import (
    BadRequest,
    InternalServerError,
    HTTPException,
)  # , UnprocessableEntity

from app.auth import create_token_for_login_user, add_token_to_response

from app.libs.crypto import check_password, hash_password

from app.models.repository import find_user_by_email, insert_user

from app.routes.models import LoginSchema, RegisterUser

from app.services.logger import LoggerService

from app.utils.random import generate_random_hash
from app.utils.clear_user import clear_user

auth_routes = Blueprint("auth", __name__, url_prefix="/auth")
logger = LoggerService()


@auth_routes.post("/login")
def login():
    try:
        login_user = LoginSchema.model_validate(request.json)

        email_user = login_user.email
        password_user = login_user.password

        user = find_user_by_email(email_user)

        if not user:
            logger.log(
                route=str(request.url.path),
                method=request.method,
                message=f"Login - User not found: {email_user}",
                level="warning",
            )

            raise BadRequest("Email ou senha inválidos")

        hash_password = user.password

        if not check_password(password_user, hash_password):
            logger.log(
                route=str(request.url.path),
                method=request.method,
                message=f"Login - Invalid password: {email_user}",
                level="warning",
            )

            raise BadRequest("Email ou senha inválidos")

        random_code_session = generate_random_hash()

        token, refresh_token = create_token_for_login_user(
            email_user, random_code_session
        )

        user_clear = clear_user(user)

        logger.log(
            route=str(request.url.path),
            method=request.method,
            message=f"Login - Successfully login: {email_user}",
        )
        
        resp = make_response(
            jsonify({"user": user_clear, "token": token}),
            200
        )
        
        add_token_to_response(resp, refresh_token)
        
        return resp
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.log(
            route=str(request.url.path),
            method=request.method,
            message=f"Login - Error server login user: {e}",
            level="error",
        )

        raise InternalServerError("Falha do servidor ao realizar login")


@auth_routes.post("/register")
def register():
    try:
        register_user = RegisterUser.model_validate(request.json)

        email_user = register_user.email

        user = find_user_by_email(email_user)

        if user:
            logger.log(
                route=str(request.url.path),
                method=request.method,
                message=f"Register - User already exists: {email_user}",
                level="warning",
            )

            raise BadRequest({"msg": "Usuário existente"})

        password_hash = hash_password(register_user.password)

        insert_user(
            email=email_user, 
            name=register_user.name, 
            password=password_hash
        )

        logger.log(
            route=str(request.url.path),
            method=request.method,
            message=f"Register - Successfully registered: {email_user}",
        )

        return {"msg": "Usuário criado"}, 201

    except HTTPException as e:
        raise e
    except Exception as e:
        logger.log(
            route=str(request.url.path),
            method=request.method,
            message=f"Register - Error server registering user: {e}",
            level="error",
        )

        raise InternalServerError("Falha ao realizar cadastro")
