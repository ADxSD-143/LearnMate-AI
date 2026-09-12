from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config import settings

DATABASE_URL = settings.DATABASE_URL

# The engine is responsible for talking to PostgreSQL. It manages the low-level connection.
engine = create_engine(DATABASE_URL)

# SessionLocal is a factory for creating individual database session instances per request.
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

# declarative_base() creates the Base class for all SQLAlchemy ORM models.
Base = declarative_base()
