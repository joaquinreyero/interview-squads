from datetime import datetime, timedelta

from fastapi.security import HTTPBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from src.config import Settings
from src.utils import errors
from src.schemas import auth as schema


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
token_auth_scheme = HTTPBearer()


def hash_password(password: str):
    return pwd_context.hash(password)


def verify(plain_password, hashed_password):
    verified = pwd_context.verify(plain_password, hashed_password)
    if not verified:
        raise errors.BadRequest("Invalid credentials.")
    return


def create_access_token(user_id):
    exp = datetime.utcnow() + timedelta(minutes=Settings().ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {
        "expiration_date": str(exp),
        "is_active": True,
        "user_id": user_id,
    }
    encoded_jwt = jwt.encode(to_encode, Settings().TOKEN_SECRET_KEY, algorithm=Settings().TOKEN_ALGORITHM)
    data = schema.TokenData(
        token=encoded_jwt,
        expiration_date=str(exp),
        is_active=True,
        user_id=user_id,
    )
    return data


def verify_token(token: str):
    try:
        payload = jwt.decode(token, Settings().TOKEN_SECRET_KEY, algorithms=[Settings().TOKEN_ALGORITHM])
        user: int = payload.get("user_id")
        expiration_date_str: str = payload.get("expiration_date")
        expiration_date = datetime.strptime(expiration_date_str, "%Y-%m-%d %H:%M:%S.%f")
        is_active: bool = payload.get("is_active")
        if user is None:
            raise errors.BadRequest("Invalid token.")
        if expiration_date < datetime.utcnow():
            raise errors.BadRequest("Token expired.")
        if not is_active:
            raise errors.BadRequest("Token is not active.")

        token_data = schema.TokenData(
            token=token,
            expiration_date=payload.get("expiration_date"),
            is_active=payload.get("is_active"),
            user_id=payload.get("user_id")
        )
        return token_data
    except JWTError:
        raise errors.BadRequest("Error decoding token.")
