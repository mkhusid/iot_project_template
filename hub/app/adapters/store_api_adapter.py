import json
import logging
from typing import List

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
            # Convert the list of ProcessedAgentData to a list of dictionaries
            data_to_save = [data.model_dump(mode="json") for data in processed_agent_data_batch]

            # Send a POST request to the Store API
            response = requests.post(
                f"{self.api_base_url}/road-data/",
                headers={"Content-Type": "application/json"},
                data=json.dumps(data_to_save),
            )
            # Check if the request was successful
            if response.status_code == 200:
                logging.info("Data saved successfully to Store API")
                return True
            else:
                logging.error("Failed to save data: %s - %s", response.status_code, response.text)
                return False
        except pydantic_core.ValidationError as e:
            logging.error("Validation error: %s", e)
            return False
        except Exception as e:
            logging.error("An error occurred: %s", e)
            return False
