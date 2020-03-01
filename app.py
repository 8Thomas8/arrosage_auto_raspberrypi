import RPi.GPIO as GPIO
import datetime
import time

init = False

# Status du dernier arrosage
lw_status_code = 1

# Selectionne le type de schema des GPIO
GPIO.setmode(GPIO.BOARD)


# Verifie le dernier arrosage
def get_last_watered():
    try:
        global lw_status_code
        # Ouvre le fichier en lecture
        f = open("last_watered.txt", "r")
        lw_status_code = 0
        return f.readline()
    except len(lw_status_code) != 0:
        return "JAMAIS"


# Recupere le status du pin definit
def get_status(pin=8):
    # Set la direction du pin
    GPIO.setup(pin, GPIO.IN)
    return GPIO.input(pin)


# Initialise le status du pin definit
def init_output(pin):
    # Set la direction du pin
    GPIO.setup(pin, GPIO.OUT)
    # Set la tension qui sort du pin
    GPIO.output(pin, GPIO.LOW)
    GPIO.output(pin, GPIO.HIGH)

# Function auto_water(delay = 5, pump_pin = 5, water_sensor_pin = 8)

# Function pump_on(pump_pin = 7, delay = 1)
