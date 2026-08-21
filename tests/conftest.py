import os
import sys
app_dir = os.path.join(os.path.dirname(__file__), "..")
sys.path.append(app_dir)

import pytest
import hashlib
import base64
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import Session, sessionmaker
from app.models import Base, User
from app.schemas import DecodedToken
from app.main import app
from app.database import get_db
from app.cruds.user import get_current_user


@pytest.fixture()
def session_fixture():
    engine = create_engine(
        url = "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )
    Base.metadata.create_all(engine)

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    try:
        salt = base64.b64encode(os.urandom(32))
        hashed_password = hashlib.pbkdf2_hmac("sha256", "123abc".encode(), salt, 1000).hex()
        user1 = User(password=hashed_password, salt = salt.decode(), last_name="Yamada", first_name="Taro", email="yamada@com")
        user2 = User(password=hashed_password, salt = salt.decode(), last_name="Suzuki", first_name="Hanako", email="suzuki@com")
        db.add(user1)
        db.add(user2)
        db.commit()
        yield db
    finally:
        db.close()

@pytest.fixture()
def user_fixture():
    return DecodedToken(user_id=1)

@pytest.fixture()
def client_fixture(session_fixture: Session, user_fixture: DecodedToken):
    def override_get_db():
        return session_fixture

    def override_get_current_user():
        return user_fixture

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_user

    client = TestClient(app)

    yield client

    app.dependency_overrides.clear()
