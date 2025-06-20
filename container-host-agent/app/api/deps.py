from fastapi import Header
from app.core.security import validate_server_token

def get_server_key(x_server_key: str = Header(..., alias="X-Server-Key")):
    validate_server_token(x_server_key)
    return x_server_key
