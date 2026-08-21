from datetime import datetime
from sqlalchemy import Column, Integer, String, Enum, DateTime
from app.database import Base
from app.schemas import Roles

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    password = Column(String, nullable=False)
    salt = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    email = Column(String, nullable=True)
    role = Column(Enum(Roles), nullable=False, default=Roles.STAFF)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
