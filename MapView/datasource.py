import asyncio
import json
from datetime import datetime
import websockets
from kivy import Logger
from pydantic import BaseModel, field_validator
import scipy.signal
from config import STORE_HOST, STORE_PORT

# Pydantic models

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
        if isinstance(value, datetime):
            return value
        try:
            return datetime.fromisoformat(value)
        except (TypeError, ValueError):
            raise ValueError(
                "Invalid timestamp format. Expected ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ)."
            )

class ProcessedAgentData(BaseModel):
    road_state: str
    agent_data: AgentData

class Datasource:
    def __init__(self):
        self.index = 0
        self.connection_status = None
        self._new_data = []
        asyncio.ensure_future(self.connect_to_server())

    async def connect_to_server(self):
        uri = f"ws://{STORE_HOST}:{STORE_PORT}/ws"
        while True:
            Logger.debug("CONNECT TO SERVER")
            async with websockets.connect(uri) as websocket:
                self.connection_status = "Connected"
                try:
                    while True:
                        data = await websocket.recv()
                        try:
                            parsed_data = json.loads(data)
                            self.handle_received_data(parsed_data)
                        except json.JSONDecodeError:
                            print("Received data is not valid JSON:")
                            print(data)
                except websockets.exceptions.ConnectionClosedError:
                    self.connection_status = "Disconnected"
                    Logger.debug("SERVER DISCONNECT")

    def handle_received_data(self, data):
        # Update your UI or perform actions with received data here
        parsed_items = [json.loads(item) for item in json.loads(data)]
        Logger.info(f"Received data: {parsed_items}")
        sorted_data = sorted(
            [
                ProcessedAgentData(**processed_data_json)
                for processed_data_json in parsed_items
            ],
            key=lambda v: v.agent_data.timestamp
        )
        self._new_data.extend(sorted_data)
        
    def get_new_data(self):
        Logger.debug(self._new_data)
        new_data = self._new_data
        last_gps = None
        if len(self._new_data) > 0:
            last_gps = self._new_data[-1].agent_data.gps
        self._new_data = []
        return new_data, last_gps