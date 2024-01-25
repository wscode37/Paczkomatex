import paho.mqtt.client as mqtt
from datetime import datetime
import json
from firebase_test import check_package_existence
import package_handler
import config

BROKER_HOST = "io.adafruit.com"
PORT = 1883
ADAFRUIT_USER = "266615"
ADAFRUIT_KEY = "aio_HuyN38tawpcHAQxUXkC3d3x9E8FR"
 # Replace with your actual parcel locker ID

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
        # Subscribe to the appropriate topic
        topic = f"266615/feeds/paczkomat{config.PARCEL_LOCKER_ID}"
        client.subscribe("266615/errors", qos=0)
        client.subscribe(topic, qos=0)
    else:
        print("Connection to MQTT broker failed")

def on_message(client, userdata, msg):
    try:
        # Decode the payload as JSON
        payload = msg.payload.decode("utf-8")

        # Example logic - check the package by code


        package_data = check_package_existence(payload)
        if package_data:
            print(f"Package for code {payload} found:")
            print(package_data)
            package_handler.add_receiver_package(package_data)
            # Here you can add additional handling logic, e.g., open the locker

    except Exception as e:
        print(f"Error processing message: {str(e)}")

if __name__ == "__main__":
    # Load configuration from the config file
    

    client = mqtt.Client("ParcelLockerListener")
    client.on_connect = on_connect
    client.on_message = on_message

    print("Connecting to MQTT broker")
    client.username_pw_set(ADAFRUIT_USER, password=ADAFRUIT_KEY)
    client.connect(BROKER_HOST, port=PORT, keepalive=60)

    # Blocking call to process network traffic, dispatch callbacks, and handle reconnecting
    client.loop_forever()
