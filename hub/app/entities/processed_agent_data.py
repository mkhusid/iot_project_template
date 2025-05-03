from pydantic import BaseModel
from app.entities.agent_data import AgentData


class ProcessedAgentData(BaseModel):
    road_state: str
    agent_data: AgentData

    def serialize (self) -> dict:
        return {
            "road_state": self.road_state,
            "agent_data": {
                "user_id": 0,
                "accelerometer": {
                    "x": self.agent_data.accelerometer.x,
                    "y": self.agent_data.accelerometer.y,
                    "z": self.agent_data.accelerometer.z
                },
                "gps": {
                    "latitude": self.agent_data.gps.latitude,
                    "longitude": self.agent_data.gps.longitude
                },
                "timestamp": self.agent_data.timestamp,
            }
        }