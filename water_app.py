import RPi.GPIO as GPIO
import datetime
import time

# Source: http://www.cyber-omelette.com/2017/09/automated-plant-watering.html
# Avec refacto et customisation 

# Selectionne le type de schema des GPIO
GPIO.setmode(GPIO.BOARD)

# Definition des variables
water_sensor_pin = 8
pump_pin = 7
time_pump_on = 3
delay_before_auto_watering = 5


# Verifie le dernier arrosage
def get_last_watered():
    try:
        # Ouvre le fichier en lecture
        f = open("last_watered.txt", "r")
        return f.readline()
    except IOError:
        return "JAMAIS"


# Recupere le status du pin definit
def get_status():
    # Set la direction du pin
    GPIO.setup(water_sensor_pin, GPIO.IN)
    return GPIO.input(water_sensor_pin)


# Initialise le status du pin definit
def init_output(pin):
    # Set la direction du pin
    GPIO.setup(pin, GPIO.OUT)
    # Set la tension qui sort du pin
    GPIO.output(pin, GPIO.LOW)
    GPIO.output(pin, GPIO.HIGH)


# Gere l'arrosage automatique
def auto_water():
    consecutive_water_count = 0
    init_output(pump_pin)
    print("Arrosage automatique lance, faites CTRL+C pour quitter.")
    try:
        while True:
            time.sleep(delay_before_auto_watering)
            wet = get_status()
            print("Humide (0 = oui, 1 = non)= " + str(wet))
            if wet != 0 and consecutive_water_count <= 5:
                pump_on()
                consecutive_water_count += 1
            elif wet != 0 and consecutive_water_count > 5:
                time.sleep(20)
                consecutive_water_count = 0
            else:
                consecutive_water_count = 0
    except KeyboardInterrupt:
        print("Arrosage automatique interrompu.")
        GPIO.cleanup()


# Active la pompe
def pump_on():
    init_output(pump_pin)
    # Ouvre le fichier en mode ecriture
    f = open("last_watered.txt", "w")
    f.write("Dernier arrosage {}".format(datetime.datetime.now()))
    f.close()
    # Active puis desactive la pompe
    GPIO.output(pump_pin, GPIO.LOW)
    time.sleep(time_pump_on)
    GPIO.output(pump_pin, GPIO.HIGH)
