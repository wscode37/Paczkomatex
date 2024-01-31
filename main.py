import time
from PIL import Image, ImageDraw, ImageFont
import lib.oled.SSD1331 as SSD1331
import RPi.GPIO as GPIO
import config
import package_handler
from encoder import Encoder
import delivery_service
import paho.mqtt.client as mqtt

disp = SSD1331.SSD1331()
rotary_encoder = Encoder(config.encoderLeft, config.encoderRight, callback=None)  # Możesz przekazać swoją funkcję callback, jeśli potrzebujesz

button_green_pin = config.buttonGreen  # Przykładowy numer pinu
button_red_pin = config.buttonRed  # Przykładowy numer pinu

BROKER_HOST = "io.adafruit.com"
PORT = 1883
ADAFRUIT_USER = "266615"
ADAFRUIT_KEY = "aio_HuyN38tawpcHAQxUXkC3d3x9E8FR"

client = None  # Declare the MQTT client globally

def initialize_oled():
    # Inicjalizacja OLED na początku
    disp.clear()
    disp.Init()

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


def start_screen():
    while config.depth == 0:
        font_large = ImageFont.truetype('./lib/oled/Font.ttf', 13)
        image = Image.new("RGB", (disp.width, disp.height), "BLACK")
        draw = ImageDraw.Draw(image)

        # Handle encoder rotation to update current_option
        current_option_indicator = "-" if rotary_encoder.getValue()%2 == 0 else " "
        draw.text((8, 10), f"{current_option_indicator}{config.options[0]}", font=font_large, fill="WHITE")
        
        current_option_indicator = "-" if rotary_encoder.getValue()%2 == 1 else " "
        draw.text((8, 30), f"{current_option_indicator}{config.options[1]}", font=font_large, fill="WHITE")

        disp.ShowImage(image, 0, 0)


def insert_code_screen():
    
      font_large = ImageFont.truetype('./lib/oled/Font.ttf', 13)
      image = Image.new("RGB", (disp.width, disp.height), "BLACK")
      draw = ImageDraw.Draw(image)
      draw.text((8, 10), "Podaj 4-cyfrowy kod:", font=font_large, fill="WHITE")

      while config.depth == 0:
        x = 8
        y = 30
        spacing = 10
        if config.input_position == 0:
            draw.text((x, y), rotary_encoder.getValue()%10, font=font_large, fill="WHITE")
            y += spacing
            for i in range(3):
              digit = str(config.input_code[i+1])
              draw.text((x, y), digit, font=font_large, fill="WHITE")
              y += spacing
        elif config.input_position == 1:
            draw.text((x, y), str(config.input_code[0]), font=font_large, fill="WHITE")
            y += spacing
            draw.text((x, y), rotary_encoder.getValue()%10, font=font_large, fill="WHITE")
            y += spacing
            for i in range(2):
              digit = str(config.input_code[i+2])
              draw.text((x, y), digit, font=font_large, fill="WHITE")
              y += spacing
        elif config.input_position == 2:
            for i in range(2):
              digit = str(config.input_code[i])
              draw.text((x, y), digit, font=font_large, fill="WHITE")
              y += spacing
            draw.text((x, y), rotary_encoder.getValue()%10, font=font_large, fill="WHITE")
            y += spacing
            draw.text((x, y), str(config.input_code[3]), font=font_large, fill="WHITE")
            y += spacing
        elif config.input_position == 3:
            draw.text((x, y), str(config.input_code[0]), font=font_large, fill="WHITE")
            y += spacing
            for i in range(3):
              digit = str(config.input_code[i])
              draw.text((x, y), digit, font=font_large, fill="WHITE")
              y += spacing
            draw.text((x, y), rotary_encoder.getValue()%10, font=font_large, fill="WHITE")
            y += spacing

      disp.ShowImage(image, 0, 0)

def accept_code_screen():
    while(config.depth == 2):
      font_small = ImageFont.truetype('./lib/oled/Font.ttf', 10)
      image = Image.new("RGB", (disp.width, disp.height), "BLACK")
      draw = ImageDraw.Draw(image)

      draw.text((8, 10), "Akceptuj kod", font=font_small, fill="WHITE")
      draw.text((8, 30), "Anuluj kod", font=font_small, fill="WHITE")

      disp.ShowImage(image, 0, 0)

def display_picture_screen():
    while(config.depth == 3):
      image_path = "ok.jpg"  # Default image for demonstration          
      code_to_id = 1000*config.input_code[0] + 100*config.input_code[1] + 10*config.input_code[2] + config.input_code[0]
      
      if(config.current_option == 0):
        package_data = delivery_service.check_package_existence(code_to_id)
        if package_data != None:
            image_path = "ok.jpg"
            delivery_service.add_package(package_data)
            publish_code_to_mqtt(code_to_id, package_data.getTarget())
            delivery_service.remove_package(code_to_id)   
        else:
            image_path = "bad.jpg"
      elif(config.current_option == 1):
        if(delivery_service.is_package_at_device(code_to_id)):
          image_path = "ok.jpg"
          delivery_service.remove_package(code_to_id)
          delivery_service.remove_package_from_firestore(code_to_id)
        else:
            image_path = "bad.jpg"
      image = Image.open(image_path)
      disp.ShowImage(image, 0, 0)

def publish_code_to_mqtt(package_id, target_paczkomat):
    if client is None:
        initialize_mqtt_client()

    topic = f"266615/feeds/paczkomat{target_paczkomat}"
    client.publish(topic, package_id, 0, True)


def green_button_callback(channel):
    if config.depth == 0:
        config.current_option = rotary_encoder.getValue()%2
        config.depth = 1

    elif config.depth == 1:
        config.input_code[config.input_position] = rotary_encoder.getValue()%10
        config.input_position = config.input_position + 1
        if config.input_position == 4:
            config.depth = 2  # Move to the next depth level

    elif config.depth == 2:
        config.depth = 3  # Move to the next depth level

    elif config.depth == 3:
        config.depth = 0  # Move to the start screen

def red_button_callback(channel):
    if config.depth > 0:
        config.input_code = [0, 0, 0, 0]
    config.depth = 0

def initialize_buttons():
    # Inicjalizacja GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(button_green_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(button_red_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # Konfiguracja przerwań
    GPIO.add_event_detect(button_green_pin, GPIO.FALLING, callback=green_button_callback, bouncetime=300)
    GPIO.add_event_detect(button_red_pin, GPIO.FALLING, callback=red_button_callback, bouncetime=300)

if __name__ == "__main__":
    try:
        initialize_oled()
        initialize_buttons()
        initialize_mqtt_client()

        while True:
            if config.depth == 0:
                start_screen()
            elif config.depth == 1:
                insert_code_screen()
            elif config.depth == 2:
                accept_code_screen()
            elif config.depth == 3:
                display_picture_screen()

            time.sleep(0.2)

    except KeyboardInterrupt:
        print("Przerwano program.")

    finally:
        GPIO.cleanup()  # Sprzątanie po zakończeniu programu
