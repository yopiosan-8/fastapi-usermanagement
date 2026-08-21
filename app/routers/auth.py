from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status
from app.cruds import user as user_cruds
from app.schemas import Token
from app.database import get_db

DbDependency = Annotated[Session, Depends(get_db)]
router = APIRouter(prefix="/auth", tags=["auth"])
FormDepnedency = Annotated[OAuth2PasswordRequestForm, Depends()]

@router.post("/login", status_code=status.HTTP_200_OK, response_model=Token)
async def login(db: DbDependency, form_data: FormDepnedency):
    user = user_cruds.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect userid or password.")

    token = user_cruds.create_access_token(user.id, timedelta(minutes=20))
    return {"access_token": token, "token_type": "bearer"}