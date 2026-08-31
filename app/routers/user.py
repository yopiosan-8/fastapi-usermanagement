from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from starlette import status
from app.cruds import user as user_cruds
from app.schemas import UserCreate, UserUpdate, UserResponse, DecodedToken
from app.database import get_db

DbDependency = Annotated[Session, Depends(get_db)]

UserDependency = Annotated[DecodedToken, Depends(user_cruds.get_current_user)]

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("", response_model=list[UserResponse], status_code=status.HTTP_200_OK, description="全てのユーザーを検索する")
async def find_all(db: DbDependency):
    return user_cruds.find_all(db)

@router.get("/{id}", response_model=UserResponse, status_code=status.HTTP_200_OK, description="ユーザーをID指定で検索する<br>条件に合致するユーザーが存在しない場合はエラー")
async def find_by_id(db: DbDependency, user: UserDependency, id: int):
    found_user = user_cruds.find_by_id(db, id)
    if not found_user:
        raise HTTPException(status_code=404, detail="User not found.")
    return found_user

@router.get("/", response_model=list[UserResponse], status_code=status.HTTP_200_OK, description="ユーザーをユーザー名の部分一致で検索する")
async def find_by_name(db: DbDependency, name: str):
    return user_cruds.find_by_name(db, name)

@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED, description="ユーザーを新規作成する")
async def create(db: DbDependency, user: UserDependency, user_create: UserCreate):
    return user_cruds.create(db, user_create)

@router.put("/{id}", response_model=UserResponse, status_code=status.HTTP_200_OK, description="ユーザーを情報を更新する<br>ログインユーザーによる自ユーザー情報の更新は不可<br>指定したIDのユーザーが存在しない場合はエラー")
async def update(db: DbDependency, user: UserDependency, id: int, user_update: UserUpdate):

    if user.user_id == id:
        raise HTTPException(status_code=404, detail="Cannot update yourself.")

    updated_user = user_cruds.update(db, id, user_update)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not updated.")
    return updated_user

@router.delete("/{id}", response_model=UserResponse, status_code=status.HTTP_200_OK, description="ユーザーを削除する<br>ログインユーザーによる自ユーザーの削除は不可<br>指定したIDのユーザーが存在しない場合はエラー")
async def delete(db: DbDependency, user: UserDependency, id: int):

    if user.user_id == id:
        raise HTTPException(status_code=404, detail="Cannot delete yourself.")

    deleted_user = user_cruds.delete(db, id)
    if not deleted_user:
        raise HTTPException(status_code=404, detail="User not deleted.")
    return deleted_user