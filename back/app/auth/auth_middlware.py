from functools import wraps
from flask import request, jsonify, g, current_app
from jose import JWTError

from app.libs.jwt import verify_token
from app.models.repository import find_user_by_id

def jwt_required(auto_refresh: bool = True):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            auth_header = request.headers.get("Authorization")
            
            if current_app.config.get("TESTING"):
                g.current_user = {
                    "email": "test@user.com",
                    "plan_type": "free",
                    "has_company": False,
                    "owner_email": "",
                }
                
                return f(*args, **kwargs)

            if not auth_header or not auth_header.startswith("Bearer "):
                return jsonify({
                    "detail": "Credenciais Inválidas"
                }), 401

            token = auth_header.split(" ")[1]

            try:
                payload = verify_token(token, auto_refresh=auto_refresh)

                user_id = payload.get("id")

                if not user_id:
                    return jsonify({"detail": "Credenciais Inválidas"}), 401

                user = find_user_by_id(user_id)

                if not user:
                    return jsonify({"detail": "Credenciais Inválidas"}), 401

                user_data = {
                    "id": user.id,
                    "email": user.email,
                    "name": user.name,
                    "password": user.password,
                    "session_code": user.session_code,
                    "created_at": user.created_at,
                    "updated_at": user.updated_at,
                }

                # Injeta usuário no contexto global da requisição
                g.current_user = user_data
            except JWTError:
                return jsonify({
                    "detail": "Credenciais Inválidas"
                }), 401

            return f(*args, **kwargs)

        return decorated_function
    return decorator