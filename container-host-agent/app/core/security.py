import jwt
from fastapi import HTTPException, status
from app.core.config import settings

def validate_server_token(token: str) -> None:
    try:
        jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=["HS256"],
            options={"verify_exp": False}
        )
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid server key"
        )
