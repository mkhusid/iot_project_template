''' Main entry point for the MQTT edge adapters. '''
import logging
from app.adapters.agent_mqtt_adapter import AgentMQTTAdapter
from app.adapters.hub_mqtt_adapter import HubMqttAdapter
from config import (
    MQTT_BROKER_HOST,
    MQTT_BROKER_PORT,
    MQTT_TOPIC,
    HUB_MQTT_BROKER_HOST,
    HUB_MQTT_BROKER_PORT,
    HUB_MQTT_TOPIC,
)


def main():
    ''' Main function to initialize and run the MQTT edge adapters. '''
    # Initialize the Hub MQTT adapter
    hub_mqtt_adapter = HubMqttAdapter(
        broker=HUB_MQTT_BROKER_HOST,
        port=HUB_MQTT_BROKER_PORT,
        topic=HUB_MQTT_TOPIC,
    )

    # Initialize the Agent MQTT adapter
    agent_adapter = AgentMQTTAdapter(
        broker_host=MQTT_BROKER_HOST,
        broker_port=MQTT_BROKER_PORT,
        topic=MQTT_TOPIC,
        hub_gateway=hub_mqtt_adapter  # Use the HTTP adapter for saving data
    )

    hub_adapter = HubMqttAdapter(
        broker=HUB_MQTT_BROKER_HOST,
        port=HUB_MQTT_BROKER_PORT,
        topic=HUB_MQTT_TOPIC,
    )

    agent_adapter = AgentMQTTAdapter(
        broker_host=MQTT_BROKER_HOST,
        broker_port=MQTT_BROKER_PORT,
        topic=MQTT_TOPIC,
        hub_gateway=hub_adapter,
    )
    try:
        # Connect to the MQTT broker and start listening for messages
        agent_adapter.connect()
        agent_adapter.start()
        # Keep the system running indefinitely (you can add other logic as needed)
        while True:
            pass
    except KeyboardInterrupt:
        # Stop the MQTT adapter and exit gracefully if interrupted by the user
        agent_adapter.stop()
        logging.info("System stopped.")


if __name__ == "__main__":

    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] [%(levelname)s] [%(module)s] %(message)s",
        handlers=[
            logging.StreamHandler(),  # Output log messages to the console
            logging.FileHandler("app.log"),  # Save log messages to a file
        ],
    )

    logging.info("Starting the application...")
    main()
