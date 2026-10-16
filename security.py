#security.py
from pwdlib import PasswordHash
from jose import jwt, JWTError
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer

from models.user import UserDB
from database.database_connection import get_db


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


password_hash = PasswordHash.recommended()

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(
    password: str,
    hashed_password: str
) -> bool:
    return password_hash.verify(
        password,
        hashed_password
    )


def create_access_token(data: dict) -> str:
    token = jwt.encode(
        data,
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    return token


def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        return payload

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Token was invalid or mismatched"
        )


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    payload = decode_access_token(token)

    user_id = payload.get("sub")

    current_user = db.query(UserDB).filter(
        UserDB.id == user_id
    ).first()

    if not current_user:
        raise HTTPException(
            status_code=401,
            detail="JWT access fail"
        )

    return current_user#krish@1234bvrit.in

def require_admin(current_user = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

    return current_user
"""{
  "username": "sunny12",
  "email": "krish@1234bvrit.in",
  "password": "sun12345"
}"""