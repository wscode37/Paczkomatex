import paho.mqtt.client as mqtt
import delivery_service

BROKER_HOST = "io.adafruit.com"
PORT = 1883
ADAFRUIT_USER = "266615"
ADAFRUIT_KEY = "aio_HuyN38tawpcHAQxUXkC3d3x9E8FR"

client = None

def initialize_mqtt_client():
    global client
    client = mqtt.Client("ParcelLockerListener")
    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set(ADAFRUIT_USER, password=ADAFRUIT_KEY)
    client.connect(BROKER_HOST, port=PORT, keepalive=120)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
        topic = f"266615/feeds/paczkomat{config.PARCEL_LOCKER_ID}"
        client.subscribe("266615/errors", qos=0)
        client.subscribe(topic, qos=0)
    else:
        print("Connection to MQTT broker failed")

def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode("utf-8")

        package_data = delivery_service.check_package_existence(payload)
        if package_data:
            print(f"Package for code {payload} found:")
            print(package_data)
            new_package = delivery_service.check_package_existence(package_data)
            delivery_service.add_package(new_package)
            # Additional handling logic, e.g., open the locker

    except Exception as e:
        print(f"Error processing message: {str(e)}")

def publish_code_to_mqtt(package_id, target_paczkomat):
    if client is None:
        initialize_mqtt_client()

    topic = f"266615/feeds/paczkomat{target_paczkomat}"
    client.publish(topic, package_id, 0, True)

if __name__ == "__main__":
    try:

      initialize_mqtt_client()
      package_data = delivery_service.check_package_existence(code_to_id)
      code_to_id = package_data.getId
      delivery_service.add_package(package_data)
      publish_code_to_mqtt(code_to_id, package_data.getTarget())
      delivery_service.remove_package(code_to_id)  
      
      
            

    except KeyboardInterrupt:
        print("Przerwano program.")

    finally:
        GPIO.cleanup()  # Sprzątanie po zakończeniu programu
