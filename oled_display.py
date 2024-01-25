# oled_display.py
import time
from PIL import Image, ImageDraw, ImageFont
from firebase_test import check_package_existence
import lib.oled.SSD1331 as SSD1331
import RPi.GPIO as GPIO
import config
import package_handler
import paho.mqtt.client as mqtt

disp = SSD1331.SSD1331()
rotary_encoder = config.RotaryEncoder(config.encoderLeft, config.encoderRight, config.buttonGreen)

def update_oled():
    disp.clear()

    font_large = ImageFont.truetype('./lib/oled/Font.ttf', 20)
    font_small = ImageFont.truetype('./lib/oled/Font.ttf', 13)

    image = Image.new("RGB", (disp.width, disp.height), "WHITE")
    draw = ImageDraw.Draw(image)

    draw.text((8, 0), config.options[config.current_option], font=font_large, fill="WHITE")

    if config.input_position == 4:
        # Ekran "Potwierdź kod" i "Anuluj"
        draw.text((8, 40), " ".join(map(str, config.input_code)), font=font_large, fill="WHITE")
        draw.text((8, 60), "Potwierdź kod", font=font_small, fill="WHITE")
        draw.text((8, 80), "Anuluj", font=font_small, fill="WHITE")
    else:
        # Ekran wprowadzania kodu
        draw.text((8, 40), "Podaj 4-cyfrowy kod wysyłki:", font=font_small, fill="WHITE")
        draw.text((8, 60), " ".join([str(digit) if idx == config.input_position else "_" for idx, digit in enumerate(config.input_code)]), font=font_large, fill="WHITE")

    disp.ShowImage(image, 0, 0)

def navigate_options():
    current_option = 0

    while True:
        update_oled()

        # Oczekiwanie na obrót enkodera
        rotated = rotary_encoder.get_direction()
        if rotated == 1:  # Obrót w prawo
            current_option = (current_option + 1) % len(config.options)
        elif rotated == -1:  # Obrót w lewo
            current_option = (current_option - 1) % len(config.options)

        time.sleep(0.2)  # Zapobiegaj multipleksowaniu enkodera

        # Oczekiwanie na naciśnięcie zielonego przycisku
        if GPIO.input(config.buttonGreen) == GPIO.LOW:
            config.current_option = current_option

            # Po wybraniu opcji, przeniesienie do ekranu "Podaj 4-cyfrowy kod"
            config.input_position = 0
            get_user_input()

def get_user_input():
    input_code = [0, 0, 0, 0]  # Początkowy kod

    while True:
        update_oled()

        # Oczekiwanie na obrót enkodera
        rotated = rotary_encoder.get_direction()
        if rotated == 1:  # Obrót w prawo
            input_code[config.input_position] = (input_code[config.input_position] + 1) % 10
        elif rotated == -1:  # Obrót w lewo
            input_code[config.input_position] = (input_code[config.input_position] - 1) % 10

        time.sleep(0.2)  # Zapobiegaj multipleksowaniu enkodera

        # Oczekiwanie na naciśnięcie zielonego przycisku
        if GPIO.input(config.buttonGreen) == GPIO.LOW:
            config.input_code = input_code
            config.input_position += 1

            if config.input_position == 4:
                # Po wprowadzeniu wszystkich 4 cyfr, przejście do ekranu "Potwierdź kod" i "Anuluj"
                confirm_code_screen()
                return

def confirm_code_screen():
    while True:
        update_oled()

        # Oczekiwanie na obrót enkodera
        rotated = rotary_encoder.get_direction()
        if rotated == 1 or rotated == -1:
            # Obrót enkodera na tym etapie nic nie robi, możesz dodać odpowiednie działanie
            pass

        time.sleep(0.2)  # Zapobiegaj multipleksowaniu enkodera

        # Oczekiwanie na naciśnięcie przycisku
        if GPIO.input(config.buttonGreen) == GPIO.LOW:
            # Potwierdzenie kodu
            entered_code = ''.join(map(str, config.input_code))
            print(f"Wprowadzony kod: {entered_code}")
            package_data = check_package_existence(entered_code)
            if package_data:
                print("Paczka istnieje:")
                print(package_data)
                # Tutaj możesz dodać dalszą logikę obsługi, np. otwarcie skrytki
                added_package_index = package_handler.add_package(package_data)
                publish_code_to_mqtt(entered_code, package_data['targetParcelLocker'])
            else:
                print("Paczka o podanym kodzie nie istnieje.")
            image_path = "ok.jpg"
            text = "Paczka o podanym kodzie została znaleziona"
            display_image_and_text(image_path, text)

        elif GPIO.input(config.buttonRed) == GPIO.LOW:
            # Anulowanie wprowadzonego kodu i powrót do poprzedniego ekranu
            image_path = "bad.jpg"
            text = "Nie odnaleziono paczki o podanym kodzie"
            display_image_and_text(image_path, text)

        wait_for_button_press()
            # Powrót do głównego ekranu
        config.input_position = 0
        return    

def publish_code_to_mqtt(code, target_paczkomat):
    client = mqtt.Client()
    client.username_pw_set("266615", password="aio_HuyN38tawpcHAQxUXkC3d3x9E8FR")
    client.connect("io.adafruit.com", 1883)

    topic = f"266615/feeds/paczkomat{target_paczkomat}"
    client.publish(topic, code, 0, True)
    client.disconnect()

def display_image_and_text(image_path, text):
    # Wyświetl obrazek i tekst na całym ekranie
    image = Image.open(image_path)
    disp.ShowImage(image, 0, 0)

    font_large = ImageFont.truetype('./lib/oled/Font.ttf', 20)
    draw = ImageDraw.Draw(image)
    draw.text((8, 90), text, font=font_large, fill="WHITE")

    disp.ShowImage(image, 0, 0)

def wait_for_button_press():
    # Oczekiwanie na naciśnięcie przycisku
    while True:
        if GPIO.input(config.buttonGreen) == GPIO.LOW or GPIO.input(config.buttonRed) == GPIO.LOW:
            return
        time.sleep(0.2)

if __name__ == "__main__":
    navigate_options()
    print(f"Wybrana opcja: {config.options[config.current_option]}")