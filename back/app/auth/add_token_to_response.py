from flask import Response

one_day = 60 * 60 * 24
seven_days = one_day * 7

def add_token_to_response(resp: Response, refresh_token: str):
    """Adiciona tokens de authenticação ao response, compartilhando credenciais de forma mais segura"""

    resp.set_cookie(
        key="refresh_token",
        value=refresh_token,
        max_age=seven_days,
        secure=True,
        httponly=True,
        samesite="LAX",
        path="/",
    )
