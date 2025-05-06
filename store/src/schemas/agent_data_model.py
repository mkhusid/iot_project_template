''' Pydantic models for store agent data API. '''
from datetime import datetime
from pydantic import field_validator, BaseModel


class AccelerometerDataModel(BaseModel):
    ''' Accelerometer data model. '''
    x: float
    y: float
    z: float


class GpsDataModel(BaseModel):
    ''' GPS data model. '''
    latitude: float
    longitude: float


class AgentDataModel(BaseModel):
    ''' Agent data model. '''
    user_id: int
    accelerometer: AccelerometerDataModel
    gps: GpsDataModel
 

class ProcessedAgentDataModel(BaseModel):
    ''' Processed agent data model. '''
    road_state: str
    agent_data: AgentDataModel
