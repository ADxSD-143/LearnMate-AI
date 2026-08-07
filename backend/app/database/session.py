from sqlalchemy import create_engine
"""create_engine() SQLAlchemy ka function hai jo Python application aur database ke beech communication ke liye Engine object banata hai."
 " Ye database connection ko manage karta hai aur SQL queries execute karne ka foundation provide karta ha"""

from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "postgresql://postgres:99aa88bb@localhost:5432/learnmate"

#The engine is responsible for talking to PostgreSQL. It manages the low-level connection.
engine = create_engine(DATABASE_URL)

#So the session is not the conversation. It is a temporary workspace that tracks database operations for one request.
#Request->Create Session-> Read / Add / Update / Delete objects-> commit()   ← Save changes permanently or rollback() ← Discard changes->Close Session

SessionLocal = sessionmaker(bind=engine,#Links the session directly to your database engine/connection pool.
                       autoflush=False,# Prevents SQLAlchemy from sending pending changes to the DB before every query
                       autocommit=False)#Ensures that database operations occur within an explicit transaction block rather than committing automatically after every single statement.

"""
declarative_base() creates a base class for SQLalchemy ORM models.->#ORM (Object Relational Mapping)
- Tracks all model definitions (User, Product, etc.) in 'Base.metadata'
- Maps class attributes to database table columns
- Used to execute 'Base.metadata.create_all(bind=engine)' to build tables in the DB
"""
Base = declarative_base()

