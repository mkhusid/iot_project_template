''' Module for handling data from the server via websockets. '''
import asyncio
import json
from typing import List
import websockets
from kivy import Logger
from config import STORE_HOST, STORE_PORT, USER_ID
from models import ProcessedAgentData


class DataSource:
    ''' DataSource class for handling data from server via websockets. '''

    def __init__(self):
        self.index = 0
        self.connection_status = None
        self._new_data = []
        self.uri = f"ws://{STORE_HOST}:{STORE_PORT}/ws/{USER_ID}"

        asyncio.ensure_future(self.connect_to_server())

    async def connect_to_server(self):
        ''' Connect to the server via websockets. '''
        while True:
            Logger.debug("CONNECT TO SERVER")
            async with websockets.connect(self.uri) as websocket:
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

    def handle_received_data(self, data: List[ProcessedAgentData]):
        ''' Update your UI or perform actions with received data here '''
        parsed_items = [json.loads(item) for item in json.loads(data)]
        Logger.info("Received data: %s", parsed_items)
        sorted_data = sorted(
            [
                ProcessedAgentData(**processed_data_json)
                for processed_data_json in parsed_items
            ],
            key=lambda v: v.agent_data.timestamp
        )
        self._new_data.extend(sorted_data)

    def get_new_data(self):
        ''' Returns new data and last GPS coordinates. '''
        Logger.debug(self._new_data)
        new_data = self._new_data
        last_gps = None
        if len(self._new_data) > 0:
            last_gps = self._new_data[-1].agent_data.gps
        self._new_data = []
        return new_data, last_gps
