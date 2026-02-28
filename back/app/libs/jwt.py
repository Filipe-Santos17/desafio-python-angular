from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any

import jwt
from jose import JWTError

from app.envs import envs

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    
    to_encode.update({"type": "access"})
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=envs["ACCESS_TOKEN_EXPIRE_MINUTES"] | 15 # 
        )
        
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(
        to_encode, 
        envs["SECRET_KEY"], 
        algorithm=envs["ALGORITHM"]
    )
    
    return encoded_jwt


def create_refresh_token(data: dict):
    to_encode = data.copy()
    
    to_encode.update({"type": "refresh"})
    
    expire = datetime.now(timezone.utc) + timedelta(days=7)  # 7 days for refresh token
    
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(
        to_encode, 
        envs["SECRET_KEY_REFRESH"], 
        algorithm=envs["ALGORITHM"]
    )
    
    return encoded_jwt

def verify_token(
    token: str, token_type: str = "access", auto_refresh: bool = False
) -> Dict[str, Any]:
    try:
        payload = jwt.decode(
            token, 
            envs["SECRET_KEY"], 
            algorithms=envs["ALGORITHM"],
        )
        
        email: str = payload.get("email")
        exp: int = payload.get("exp")
        
        if not email:
            raise JWTError("Token missing email claim")
            
        expiration_datetime = datetime.fromtimestamp(exp, tz=timezone.utc)
        
        if token_type == "access" and expiration_datetime < datetime.now(timezone.utc):
            if auto_refresh:
                # Create a new token 
                
                new_token_user = {
                    "email": email,
                    "exp": datetime.now(timezone.utc) + 
                    timedelta(minutes=envs["ACCESS_TOKEN_EXPIRE_MINUTES"])
                }
                
                new_token_user["token"] = create_access_token(new_token_user)
                new_token_user["should_refresh"] = True
                
                return new_token_user
            else:
                raise JWTError("Token has expired")
        
        return payload
    except jwt.ExpiredSignatureError:
        raise JWTError("Token has expired")
    except jwt.InvalidTokenError:
        raise JWTError("Invalid token")
    