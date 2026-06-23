"""
SQLite database configuration using SQLAlchemy.
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

import shutil

# Database file path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
default_dir = os.path.join(BASE_DIR, "data")
source_db = os.path.join(default_dir, "detector.db")

def is_writable(path):
    try:
        os.makedirs(path, exist_ok=True)
        test_file = os.path.join(path, '.test_write')
        with open(test_file, 'w') as f:
            f.write('test')
        os.remove(test_file)
        return True
    except Exception:
        return False

if os.environ.get("VERCEL") or not is_writable(default_dir):
    DB_PATH = "/tmp/detector.db"
    # Copy pre-existing database to /tmp if it exists and target doesn't
    if os.path.exists(source_db) and not os.path.exists(DB_PATH):
        try:
            os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
            shutil.copy(source_db, DB_PATH)
            os.chmod(DB_PATH, 0o666)
            print(f"Copied pre-existing database from {source_db} to {DB_PATH} and set writable permissions")
        except Exception as e:
            print(f"Failed to copy database to /tmp: {e}")
else:
    DB_PATH = os.path.join(default_dir, "detector.db")

# Ensure data directory exists
try:
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    if os.path.exists(DB_PATH):
        os.chmod(DB_PATH, 0o666)
except Exception as e:
    print(f"Failed to set permissions on DB path: {e}")

SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """Dependency that provides a database session."""
    init_db()  # Ensure tables are initialized
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Create all database tables."""
    from app.db_models import Prediction, TrainingRun  # noqa: F401
    Base.metadata.create_all(bind=engine)
