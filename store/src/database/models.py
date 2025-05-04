from sqlalchemy import Column, Integer, String, Float, DateTime
from src.database.core import Base


class ProcessedAgentData(Base):
    ''' SQLAlchemy model for processed agent data. '''
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
