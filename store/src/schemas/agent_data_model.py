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
    timestamp: datetime
    ''' Timestamp in ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ). '''

    @classmethod
    @field_validator("timestamp", mode="before")
    def check_timestamp(cls, value):
        if isinstance(value, datetime):
            return value
        try:
            return datetime.fromisoformat(value)
        except (TypeError, ValueError) as err:
            raise ValueError(
                "Invalid timestamp format. Expected ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ)."
            ) from err

class ProcessedAgentDataModel(BaseModel):
    ''' Processed agent data model. '''
    road_state: str
    agent_data: AgentDataModel
