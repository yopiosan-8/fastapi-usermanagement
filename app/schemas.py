from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class Roles(Enum):
    PRESIDENT = "President"
    SENIOR_MANAGER = "Senior Manager"
    SECTION_MANAGER = "Section Manager"
    STAFF = "Staff"

class UserCreate(BaseModel):
    password: str = Field(min_length=6, examples=["123abc"])
    last_name: str = Field(min_length=1, examples=["xxxx"])
    first_name: str = Field(min_length=1, examples=["xxxx"])
    email: Optional[str] = Field(None, examples=["abcde@xxx.co.jp"])

class UserUpdate(BaseModel):
    password: Optional[str] = Field(None, min_length=6, examples=["123abc"])
    last_name: Optional[str] = Field(None, min_length=1, examples=["xxxx"])
    first_name: Optional[str] = Field(None, min_length=1, examples=["xxxx"])
    email: Optional[str] = Field(None, examples=["abcde@xxx.co.jp"])
    role: Optional[Roles] = Field(None, examples=[Roles.STAFF])

class UserResponse(BaseModel):
    id: int = Field(gt=0, examples=[1])
    last_name: str = Field(min_length=1, examples=["xxxx"])
    first_name: str = Field(min_length=1, examples=["xxxx"])
    email: Optional[str] = Field(min_length=1, examples=["abcde@xxx.co.jp"])
    role: Roles = Field(examples=[Roles.STAFF])
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str

class DecodedToken(BaseModel):
    user_id: int
    