from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Read DATABASE_URL from env; default to local SQLite for dev
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")

# Build engine args conditionally so SQLite keeps check_same_thread
_engine_kwargs = {}
if DATABASE_URL.startswith("sqlite"):
    _engine_kwargs["connect_args"] = {"check_same_thread": False}
else:
    # tuned pooling for production Postgres (Neon)
    _engine_kwargs.update({"pool_size": 10, "max_overflow": 20, "pool_pre_ping": True})

engine = create_engine(DATABASE_URL, **_engine_kwargs)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()