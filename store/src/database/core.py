from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


from config import DATABASE_URL

Base = declarative_base()
# SQLAlchemy setup
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()
