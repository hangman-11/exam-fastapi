from jose import jwt, JWTError
from datetime import timedelta, datetime
from . import schemas
from fastapi import Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordBearer
from .config import settings

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_time

oauth2_scheme = OAuth2PasswordBearer('login')


def create_token(data: dict):
    data_cpy = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)

    data_cpy.update({"exp": expire})

    encode_jwt = jwt.encode(data_cpy, SECRET_KEY, algorithm=ALGORITHM)

    return encode_jwt


def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")

        if not id:
            raise credentials_exception

        token_id = schemas.TokenData(id=id)

    except JWTError:
        raise credentials_exception

    return token_id


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="unauthorized user",
                                          headers={"www Authenticate": "bearer"})
    return verify_token(token,credentials_exception)
