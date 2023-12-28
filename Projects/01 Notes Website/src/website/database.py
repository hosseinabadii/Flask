from pathlib import Path

from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from .models import Base

ROOT_PATH = Path(__file__).parent.parent
DB_NAME = "database.db"
DB_PATH = ROOT_PATH / DB_NAME

# SQLALCHEMY_DATABASE_URL = "sqlite:///./database.db"
SQLALCHEMY_DATABASE_URL = f"sqlite:///{str(DB_PATH)}"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)
Base.query = db_session.query_property()


def init_db():
    if not DB_PATH.exists():
        logger.info("Database not exists. Creating database...")
        Base.metadata.create_all(bind=engine)
        logger.info("Database created.")
    else:
        logger.info("Database is already exists.")
