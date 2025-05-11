""" Hub MQTT Adapter """
import logging
from paho.mqtt import client as mqtt_client
from app.entities.processed_agent_data import ProcessedAgentData
from app.interfaces.hub_gateway import HubGateway


class HubMqttAdapter(HubGateway):
    """
    HubMqttAdapter is an adapter for sending processed agent data to a Hub via MQTT.
    It implements the HubGateway interface.
    """
    def __init__(self, broker, port, topic):
        self.broker = broker
        self.port = port
        self.topic = topic
        self.mqtt_client = self._connect_mqtt(broker, port)

    def save_data(self, processed_data: ProcessedAgentData):
        """
        Save the processed road data to the Hub.
        Parameters:
            processed_data (ProcessedAgentData): Processed road data to be saved.
        Returns:
            bool: True if the data is successfully saved, False otherwise.
        """
        msg = processed_data.model_dump_json()
        result = self.mqtt_client.publish(self.topic, msg)
        status = result[0]
        if status == 0:
            return True
        else:
            logging.info("Failed to send message to topic %s", self.topic)
            return False

    @staticmethod
    def _connect_mqtt(broker, port):
        """Create MQTT client"""
        logging.info("CONNECT TO %s:%s", broker, port)

        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                logging.info("Connected to MQTT Broker (%s:%s)!", broker, port)
                logging.info("Details: %s, %s, %s, %s", client, userdata, flags, rc)
            else:
                logging.info("Failed to connect {broker}:{port}, return code %d\n", rc)
                exit(rc)  # Stop execution

        client = mqtt_client.Client()
        client.on_connect = on_connect
        client.connect(broker, port)
        client.loop_start()
        return client
