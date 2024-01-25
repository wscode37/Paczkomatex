# # rotary_encoder.py
# import RPi.GPIO as GPIO
# import time

# class RotaryEncoder:
#     def __init__(self, clk_pin, dt_pin, switch_pin):
#         self.clk_pin = clk_pin
#         self.dt_pin = dt_pin
#         self.switch_pin = switch_pin

#         GPIO.setup(clk_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#         GPIO.setup(dt_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#         GPIO.setup(switch_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#         self.clk_state = GPIO.input(clk_pin)
#         self.dt_state = GPIO.input(dt_pin)

#     def get_direction(self):
#         clk_state_new = GPIO.input(self.clk_pin)
#         dt_state_new = GPIO.input(self.dt_pin)

#         if clk_state_new != self.clk_state or dt_state_new != self.dt_state:
#             # Obrót enkodera zarejestrowany
#             if self.clk_state == 0 and dt_state_new == 0:
#                 return 1  # Obrót w prawo
#             elif self.dt_state == 0 and clk_state_new == 0:
#                 return -1  # Obrót w lewo

#         self.clk_state = clk_state_new
#         self.dt_state = dt_state_new

#         return 0  # Brak ruchu enkodera
