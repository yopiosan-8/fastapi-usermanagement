from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import get_settings

#SQLALCHEMY_DATABASE_URL = get_settings().sqlalchemy_database_url
SQLALCHEMY_DATABASE_URL = "postgresql://fastapiuser:fastapipass@watanabe-user-management.cuf82id02mnx.ap-northeast-1.rds.amazonaws.com:5432/usermanagement"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()