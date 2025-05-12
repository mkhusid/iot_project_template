import logging
from typing import List
from redis import Redis
import paho.mqtt.client as mqtt

from app.adapters.store_api_adapter import StoreApiAdapter
from app.entities.processed_agent_data import ProcessedAgentData
from config import (
    STORE_API_BASE_URL,
    REDIS_HOST,
    REDIS_PORT,
    BATCH_SIZE,
    MQTT_TOPIC,
    MQTT_BROKER_HOST,
    MQTT_BROKER_PORT,
)

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] [%(module)s] %(message)s",
    handlers=[
        logging.StreamHandler(),  # Output log messages to the console
        logging.FileHandler("app.log"),  # Save log messages to a file
    ],
)


def run_mqtt_hub(client: mqtt.Client = None, redis_client: Redis = None,
                 store_adapter: StoreApiAdapter = None):
    """Main function to run the MQTT client and publish data in an infinite loop"""

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            logging.info("Connected to MQTT broker")
            client.subscribe(MQTT_TOPIC)
        else:
            logging.info("Failed to connect to MQTT broker with code: %s", rc)

    def on_message(client, userdata, msg):
        try:
            payload: str = msg.payload.decode("utf-8")
            print("Received message:", payload)
            # Create ProcessedAgentData instance with the received data
            processed_agent_data = ProcessedAgentData.model_validate_json(
                payload, strict=True
            )

            redis_client.lpush(
                "processed_agent_data", processed_agent_data.model_dump_json()
            )
            processed_agent_data_batch: List[ProcessedAgentData] = []
            if redis_client.llen("processed_agent_data") >= BATCH_SIZE:
                for _ in range(BATCH_SIZE):
                    processed_agent_data = ProcessedAgentData.model_validate_json(
                        redis_client.lpop("processed_agent_data")
                    )
                    processed_agent_data_batch.append(processed_agent_data)
            if len(processed_agent_data_batch) > 0:
                store_adapter.save_data(processed_agent_data_batch=processed_agent_data_batch)
                return {"status": "ok"}

        except ConnectionError as ce:
            logging.info("Connection error: %s", ce)
        except Exception as e:
            logging.info("Error processing MQTT message: %s", e)

    # Set up MQTT client callbacks
    client.on_connect = on_connect
    client.on_message = on_message

    # Connect to the MQTT broker
    client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT)

    # Start the MQTT loop
    client.loop_forever()


if __name__ == "__main__":

    logging.info("Starting Hub Service via MQTT Client")
    client_ = mqtt.Client()
    # Create an instance of the Redis using the configuration
    redis_client_ = Redis(host=REDIS_HOST, port=REDIS_PORT)
    # Create an instance of the StoreApiAdapter using the configuration
    store_adapter_ = StoreApiAdapter(api_base_url=STORE_API_BASE_URL)
    # Create an instance of the AgentMQTTAdapter using the configuration

    run_mqtt_hub(client_, redis_client_, store_adapter_)
