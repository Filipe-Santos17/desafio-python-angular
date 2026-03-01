from app.libs.jwt import create_access_token, create_refresh_token

def create_token_for_login_user(id: int, random_code_session: str):
    """Cria tokens de credenciais"""

    token = create_access_token(
        {"id": id, "code_session": random_code_session}
    )

    refresh_token = create_refresh_token(
        {"id": id, "code_session": random_code_session}
    )

    return token, refresh_token


