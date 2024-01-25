# config.py
#!/usr/bin/env python3
# pylint: disable=no-member

import RPi.GPIO as GPIO

PARCEL_LOCKER_ID = 1  # Adjust this based on your parcel locker ID
MQTT_FEED = f"paczkomat/{PARCEL_LOCKER_ID}"

# Konfiguracja pinów GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Konfiguracja pinów dla diod LED
led1 = 13
led2 = 12
led3 = 19
led4 = 26
GPIO.setup(led1, GPIO.OUT)
GPIO.setup(led2, GPIO.OUT)
GPIO.setup(led3, GPIO.OUT)
GPIO.setup(led4, GPIO.OUT)

# Konfiguracja pinów dla przycisków, enkodera i buzzeru
buttonRed = 5
buttonGreen = 6
encoderLeft = 17
encoderRight = 27
buzzerPin = 23
GPIO.setup(buttonRed, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(buttonGreen, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(encoderLeft, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(encoderRight, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(buzzerPin, GPIO.OUT)
GPIO.output(buzzerPin, 1)

# Konfiguracja pinu dla WS2812
ws2812pin = 8

# Inne zmienne konfiguracyjne
options = ["Nadaj paczkę", "Odbierz paczkę"]
current_option = 0

input_code = [0, 0, 0, 0]
input_position = 0


device_packages = [None, None, None, None, None]
# ... (inne zmienne konfiguracyjne)

class RotaryEncoder:
    def __init__(self, clk_pin, dt_pin, switch_pin):
        self.clk_pin = clk_pin
        self.dt_pin = dt_pin
        self.switch_pin = switch_pin

        GPIO.setup(clk_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(dt_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(switch_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        self.clk_state = GPIO.input(clk_pin)
        self.dt_state = GPIO.input(dt_pin)

    def get_direction(self):
        clk_state_new = GPIO.input(self.clk_pin)
        dt_state_new = GPIO.input(self.dt_pin)

        if clk_state_new != self.clk_state or dt_state_new != self.dt_state:
            # Obrót enkodera zarejestrowany
            if self.clk_state == 0 and dt_state_new == 0:
                return 1  # Obrót w prawo
            elif self.dt_state == 0 and clk_state_new == 0:
                return -1  # Obrót w lewo

        self.clk_state = clk_state_new
        self.dt_state = dt_state_new

        return 0  # Brak ruchu enkodera

# ... (inne funkcje, klasy lub zmienne konfiguracyjne, jeśli są potrzebne)

# Konfiguracja enkodera
rotary_encoder = RotaryEncoder(encoderLeft, encoderRight, buttonGreen)
