"""Initialize database connection"""
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = ""

if "pytest" not in sys.modules:
    # If not running in testing environment
    assert DATABASE_URL != "", "SQLALCHEMY_DATABASE_URL must not be empty"
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Database Dependency Injection"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
