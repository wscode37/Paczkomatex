import paho.mqtt.client as mqtt
import time
import json

BROKER_HOST = "io.adafruit.com"
PORT = 1883
ADAFRUIT_USER = "266615"
ADAFRUIT_KEY = "aio_HuyN38tawpcHAQxUXkC3d3x9E8FR"
#PARCEL_LOCKER_ID = 1  # Replace with your actual parcel locker ID

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        client.connected_flag = True
        print("Connected OK")
    else:
        print("Bad connection Returned code=", rc)

mqtt.Client.connected_flag = False

client = mqtt.Client("ParcelLockerPublisher")
client.on_connect = on_connect

print("Connecting to broker ", BROKER_HOST)
client.username_pw_set(ADAFRUIT_USER, password=ADAFRUIT_KEY)
client.connect(BROKER_HOST, port=PORT)
client.loop_start()

while not client.connected_flag:
    print("Waiting for connection")
    time.sleep(1)

try:
    while True:
        # Simulating package data
        package_data = {
            'senderName': 'John Doe',
            'receiverEmail': 'receiver@example.com',
            'receiverSurname': 'Receiver',
            'senderEmail': 'sender@example.com',
            'senderSurname': 'Sender',
            'targetParcelLocker': 2,
            'receiverName': 'Jane Doe'
        }
        id = "1235"
        target_paczkomat = package_data.get('targetParcelLocker', None)
        # Convert package data to JSON
        json_package_data = json.dumps(package_data)
        # Publish the package data to the corresponding parcel locker feed
        topic = f"266615/feeds/paczkomat{target_paczkomat}"

        client.publish(topic, id, 0, True)

        print("Package data published:", json_package_data)
        time.sleep(5)
except KeyboardInterrupt:
    print('Stopping Parcel Locker Publisher')

client.loop_stop()
client.disconnect()
