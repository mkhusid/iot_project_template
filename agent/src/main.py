from datetime import datetime
import paho.mqtt.client as mqtt
import time
from schema.aggregated_data_schema import AggregatedDataSchema
from schema.gps_schema import GpsSchema
from schema.accelerometer_schema import AccelerometerSchema
from file_datasource import FileDatasource
import config


def connect_mqtt(broker, port):
    """Create MQTT client"""
    print(f"CONNECT TO {broker}:{port}")

    def on_connect(client, userdata, flags, rc, properties=None):
        if rc == 0:
            print(f"Connected to MQTT Broker ({broker}:{port})!")
            print("[INFO] Client: %s", client)
            print("[INFO] Userdata: %s", userdata)
            print("[INFO] Flags: %s", flags)
            print("[INFO] Properties: %s", properties)
        else:
            print("Failed to connect {broker}:{port}, return code %d\n", rc)
            exit(rc)  # Stop execution

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.connect(broker, port)
    client.loop_start()
    return client


def publish(client, topic, datasource, delay):
    """Publish data to MQTT broker"""
    data = datasource.read()
    print(f"Data: {data}")
    gps = GpsSchema(latitude=data.gps.latitude, longitude=data.gps.longitude)
    acc = AccelerometerSchema(
        x=data.accelerometer.x,
        y=data.accelerometer.y,
        z=data.accelerometer.z)
    msg = AggregatedDataSchema(accelerometer=acc,
                                gps=gps,
                                timestamp=str(data.timestamp),
                                user_id=str(data.user_id)).model_dump_json()
    result = client.publish(topic, msg)
    status = result[0]

    if status == 0:
        print(f"Send `{msg}` to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")

    time.sleep(delay)



def run():
    '''Main function to run the MQTT client and publish data in infinity loop'''
    client = connect_mqtt(config.MQTT_BROKER_HOST, config.MQTT_BROKER_PORT)
    accerelometer_file = './src/data/accelerometer.csv'
    gps_file = './src/data/gps.csv'

    with open(gps_file, 'r', encoding='utf-8') as gps_file,\
            open(accerelometer_file, 'r', encoding='utf-8') as accerelometer_file:
        while True:
            datasource = FileDatasource(accerelometer_file, gps_file)
            publish(client, config.MQTT_TOPIC, datasource, delay=config.DELAY)

if __name__ == "__main__":
    run()
