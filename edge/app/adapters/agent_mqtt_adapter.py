""" Agent MQTT Adapter """
import logging
import paho.mqtt.client as mqtt
from app.interfaces.agent_gateway import AgentGateway
from app.entities.agent_data import AgentData
from app.usecases.data_processing import process_agent_data
from app.interfaces.hub_gateway import HubGateway


class AgentMQTTAdapter(AgentGateway):
    """ AgentMQTTAdapter is an adapter for receiving agent data from an MQTT broker.
    It implements the AgentGateway interface.
    It processes the received data and sends it to a Hub via a HubGateway.
    """

    def __init__(
        self,
        broker_host,
        broker_port,
        topic,
        hub_gateway: HubGateway,
        batch_size=10,
    ):
        self.batch_size = batch_size
        # MQTT
        self.broker_host = broker_host
        self.broker_port = broker_port
        self.topic = topic
        self.client = mqtt.Client()
        # Hub
        self.hub_gateway = hub_gateway

    def on_connect(self, client, userdata, flags, rc):
        """Callback for when the client receives a CONNACK response from the server."""
        if rc == 0:
            logging.info("Connected to MQTT broker. Topic: %s", self.topic)
            logging.info("Details: %s, %s, %s, %s", client, userdata, flags, rc)
            self.client.subscribe(self.topic)
        else:
            logging.info("Failed to connect to MQTT broker with code: %s", rc)

    def on_message(self, client, userdata, msg):
        """Processing agent data and sent it to hub gateway"""
        try:
            logging.info("Received message on TOPIC: %s", msg.topic)
            logging.info("Message payload: %s", msg.payload)
            payload: str = msg.payload.decode("utf-8")
            # Create AgentData instance with the received data
            agent_data = AgentData.model_validate_json(payload, strict=True)
            # Process the received data (you can call a use case here if needed)
            processed_data = process_agent_data(agent_data)
            # Store the agent_data in the database (you can send it to the data processing module)

            if not self.hub_gateway.save_data(processed_data):
                logging.error("Hub is not available")
        except Exception as e:
            logging.info(f"Error processing MQTT message: {e}")

    def connect(self):
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(self.broker_host, self.broker_port, 60)

    def start(self):
        self.client.loop_start()

    def stop(self):
        self.client.loop_stop()
