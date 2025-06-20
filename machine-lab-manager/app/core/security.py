import datetime, uuid, hashlib, secrets, jwt
from passlib.context import CryptContext
from app.core.config import get_settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
settings = get_settings()


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    return pwd_context.verify(password, password_hash)


def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()


def create_admin_token(user_id: str, exp_minutes: int | None = None) -> str:
    """
    Build a JWT. If `exp_minutes` is None the token has **no expiry** (for long-lived
    config usage). Otherwise add an `exp` claim.
    """
    now = datetime.datetime.now()
    payload = {
        "sub": user_id,
        "role": "admin",
        "iat": now,
        "jti": str(uuid.uuid4()),
    }
    if exp_minutes is not None:
        payload["exp"] = now + datetime.timedelta(minutes=exp_minutes)

    return jwt.encode(payload, settings.jwt_secret, algorithm="HS256")
