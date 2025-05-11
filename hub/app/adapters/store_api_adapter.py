import json
import logging
from typing import List
from datetime import datetime

import pydantic_core
import requests

from app.entities.processed_agent_data import ProcessedAgentData
from app.interfaces.store_gateway import StoreGateway


class StoreApiAdapter(StoreGateway):
    def __init__(self, api_base_url):
        self.api_base_url = api_base_url

    def save_data(self, processed_agent_data_batch: List[ProcessedAgentData]) -> bool:
        """
        Save the processed road data to the Store API.
        Parameters:
            processed_agent_data_batch (dict): Processed road data to be saved.
        Returns:
            bool: True if the data is successfully saved, False otherwise.
        """
        try:
            # Validate the processed agent data batch
            sent_data = [processed_agent_data.serialize() for processed_agent_data in processed_agent_data_batch]
            response = requests.post(self.api_base_url + "/store/",
                                     data=json.dumps(sent_data))

            if response.ok:
                logging.info(f"Data saved successfully: {response.status_code}")
                return True
            logging.error(f"Failed to save data: {response.status_code} - {response.text}")
            return False

        except pydantic_core.ValidationError as e:
            logging.error(f"Validation error: {e}")
            return False
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return False
