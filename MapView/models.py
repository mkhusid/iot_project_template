# pylint: disable=missing-docstring
''' Pydantic Models for the MapView application. '''
from datetime import datetime
from pydantic import BaseModel, field_validator

class AccelerometerData(BaseModel):
    x: float
    y: float
    z: float


class GpsData(BaseModel):
    latitude: float
    longitude: float


class AgentData(BaseModel):
    user_id: int
    accelerometer: AccelerometerData
    gps: GpsData
    timestamp: datetime

    @classmethod
    @field_validator("timestamp", mode="before")
    def check_timestamp(cls, value):
        """Parse the timestamp to a datetime object."""
        if isinstance(value, datetime):
            return value
        try:
            return datetime.fromisoformat(value)
        except (TypeError, ValueError) as exc:
            raise ValueError(
                "Invalid timestamp format. Expected ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ)."
            ) from exc


class ProcessedAgentData(BaseModel):
    road_state: str
    agent_data: AgentData
