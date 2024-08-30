from flask import Flask, render_template
from rpi_lcd import LCD
from time import sleep
import Adafruit_ADS1x15
import RPi.GPIO as GPIO

app = Flask(__name__)

# Initialize LCD
lcd = LCD()

# Create an ADS1115 ADC object
adc = Adafruit_ADS1x15.ADS1115()

# Set the gain to ±4.096V (adjust if needed)
GAIN = 1

# Single threshold for wet/dry classification (adjust if needed)
THRESHOLD = 10000

# GPIO pin connected to the relay module to control the pump
RELAY_PIN = 12

def wet_dry_level(soil_moisture):
    if soil_moisture > THRESHOLD:
        return "DRY"
    else:
        return "WET"

def activate_pump():
    level = wet_dry_level(raw_value)

    if level == "WET":
        GPIO.output(RELAY_PIN, GPIO.HIGH)  # Turn off the pump
        lcd.text("PUMP: OFF", 1)
        lcd.text("SOIL: WET", 2)
    else:
        GPIO.output(RELAY_PIN, GPIO.LOW)  # Turn on the pump
        lcd.text("PUMP: ON", 1)
        lcd.text("SOIL: DRY", 2)
        sleep(5)  # Keep the pump on for 5 seconds
        GPIO.output(RELAY_PIN, GPIO.HIGH)  # Turn off the pump
        lcd.text("PUMP: OFF", 1)
        lcd.text("SOIL: DRY", 2)

# Setup GPIO mode and relay pin as output
GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY_PIN, GPIO.OUT)

@app.route('/')
def index():
    """Main page."""
    soil_status, pump_status = get_status()
    return render_template('data.html', soil_status=soil_status, pump_status=pump_status)

@app.route('/data')
def data():
    """Route for providing sensor and pump status."""
    soil_status, pump_status = get_status()
    return f"Pompa este: {pump_status}\nSolul este: {soil_status}"

def get_status():
    """Funcție pentru a obține starea senzorului și a pompei."""
    # Read the raw analog value from channel A3
    raw_value = adc.read_adc(3, gain=GAIN)

    # Activate the pump based on soil moisture
    activate_pump()

    # Print the results
    level = wet_dry_level(raw_value)
    print("Raw Value: {} \t Wet-Dry Level: {}".format(raw_value, level))

    return wet_dry_level(raw_value), "OFF" if GPIO.input(RELAY_PIN) else "ON"

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()
        lcd.clear()
