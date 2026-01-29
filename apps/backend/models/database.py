# models/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
from ..config import settings
import mariadb

# SQLAlchemy setup - Use SQLite for development
DATABASE_URL = "sqlite:///./green_jobs.db"

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    echo=settings.debug
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db() -> Generator[Session, None, None]:
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    """Create all tables"""
    Base.metadata.create_all(bind=engine)

# Raw MariaDB connection for vector operations
def get_mariadb_connection():
    """Get raw MariaDB connection for vector operations"""
    try:
        conn = mariadb.connect(
            user=settings.db_user,
            password=settings.db_password,
            host=settings.db_host,
            port=settings.db_port,
            database=settings.db_name
        )
        return conn
    except mariadb.Error as e:
        print(f"MariaDB connection error: {e}")
        return None