# backend/models.py
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.types import JSON
from datetime import datetime

DATABASE_URL = "sqlite:///./backend/database.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String)
    google_sub = Column(String, nullable=False, unique=True, index=True)
    picture = Column(String)

class PromptCache(Base):
    __tablename__ = "prompt_cache"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)  # Optional, for user-specific caching
    original_prompt = Column(Text, nullable=False)
    rewritten_prompt = Column(Text, nullable=False)
    included_categories = Column(JSON, nullable=False)
    excluded_categories = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)