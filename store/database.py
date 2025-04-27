from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base


from config import DATABASE_URL

Base = declarative_base()
# SQLAlchemy setup
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()


# SQLAlchemy model
class ProcessedAgentDataInDB(Base):
    __tablename__ = "processed_agent_data"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    road_state = Column(String)
    user_id = Column(Integer)
    x = Column(Float)
    y = Column(Float)
    z = Column(Float)
    latitude = Column(Float)
    longitude = Column(Float)
    timestamp = Column(DateTime)


Base.metadata.create_all(engine)
