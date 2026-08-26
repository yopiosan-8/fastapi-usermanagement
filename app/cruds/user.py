from datetime import datetime, timedelta
import hashlib
import base64
import os
from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy import or_
from sqlalchemy.orm import Session
from app.schemas import UserCreate, Roles, UserUpdate, DecodedToken
from app.models import User
from app.config import get_settings

ALGORITHM = "HS256"
SECRET_KEY = get_settings().secret_key

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def find_all(db: Session):
    return db.query(User).order_by(User.id)

def find_by_id(db: Session, id: int):
    return db.query(User).filter(User.id == id).first()

def find_by_name(db: Session, name: str):
    return db.query(User).filter(or_(User.last_name.like(f"%{name}%"), User.first_name.like(f"%{name}%"))).all()

def create(db: Session, user_create: UserCreate):
    salt = base64.b64encode(os.urandom(32))
    hashed_password = hashlib.pbkdf2_hmac("sha256", user_create.password.encode(), salt, 1000).hex()

    new_user = User(
        password = hashed_password,
        salt = salt.decode(),
        last_name = user_create.last_name,
        first_name = user_create.first_name,
        email = user_create.email
    )
    db.add(new_user)
    db.commit()
    return new_user

def update(db: Session, id: int, user_update: UserUpdate):
    user = find_by_id(db, id)
    if user is None:
        return None

    if user_update.password is not None:
        salt = base64.b64encode(os.urandom(32))
        user.password = hashlib.pbkdf2_hmac("sha256", user_update.password.encode(), salt, 1000).hex()
        user.salt = salt.decode()

    user.last_name = user.last_name if user_update.last_name is None else user_update.last_name
    user.first_name = user.first_name if user_update.first_name is None else user_update.first_name
    user.email = user.email if user_update.email is None else user_update.email
    user.role = user.role if user_update.role is None else user_update.role

    db.add(user)
    db.commit()

    return user

def delete(db: Session, id: int):
    user = find_by_id(db, id)
    if user is None:
        return None

    db.delete(user)
    db.commit()

    return user

def authenticate_user(db: Session, id: int, password: str):
    user = db.query(User).filter(User.id == id).first()

    if not user:
        return None

    hashed_password = hashlib.pbkdf2_hmac("sha256", password.encode(), user.salt.encode(), 1000).hex()

    if user.password != hashed_password:
        return None

    return user

def create_access_token(user_id: int, expires_delta: timedelta):
    expires = datetime.now() + expires_delta
    payload = {"id": user_id, "exp": expires}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("id")
        if user_id is None:
            return None
        return DecodedToken(user_id=user_id)
    except JWTError:
        raise JWTError