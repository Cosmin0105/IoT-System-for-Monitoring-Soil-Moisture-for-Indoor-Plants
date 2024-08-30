from flask import Flask, render_template, Response, request, redirect, url_for
import cv2
from rpi_lcd import LCD
from time import sleep
import Adafruit_ADS1x15
import RPi.GPIO as GPIO
import matplotlib.pyplot as plt  
import pymysql.cursors

app = Flask(__name__)

# Initialize LCD
lcd = LCD()

# Create an ADS1115 ADC object
adc = Adafruit_ADS1x15.ADS1115()

# Set the gain to ±4.096V (adjust if needed)
GAIN = 1

# Single threshold for wet/dry classification (adjust if needed)
threshold = 10000

# GPIO pin connected to the relay module to control the pump
RELAY_PIN = 12
# GPIO pin connected to the relay module to control the electrovalve
RELAY_PIN_ELECTROVALVA = 6

# Setup GPIO mode and relay pin as output
GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY_PIN, GPIO.OUT)
GPIO.setup(RELAY_PIN_ELECTROVALVA, GPIO.OUT)

# Generate and save the plot at startup
plt.clf()  # Clear the figure to prevent overlapping plots
# Generate data for the plot
x_data = []  # Store x values (time)
y_data = []  # Store y values (raw ADC values)
plt.xlabel('Time')
plt.ylabel('Raw Value')
plt.title('Real-time Raw Value Plot')


# Define your MySQL connection parameters
mysql_host = '127.0.0.1'
mysql_user = 'testuser'
mysql_password = 'PASSword*123'
mysql_db = 'login'




# Function to save data to database
def save_data_to_db(raw_value, soil_status, pump_status):
    connection = pymysql.connect(host=mysql_host,
                                 user=mysql_user,
                                 password=mysql_password,
                                 db=mysql_db,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            # SQL query to insert data into SenzorData table
            sql = "INSERT INTO SensorData (raw_value, soil_status, pump_status) VALUES (%s, %s, %s)"
            cursor.execute(sql, (raw_value, soil_status, pump_status))
        connection.commit()
    finally:
        connection.close()

def wet_dry_level(soil_moisture, threshold):
    if soil_moisture > threshold:
        return "DRY"
    else:
        return "WET"

def activate_pump(raw_value, threshold):
    level = wet_dry_level(raw_value, threshold)

    if level == "WET":
        GPIO.output(RELAY_PIN, GPIO.HIGH)  # Turn off the pump
        GPIO.output(RELAY_PIN_ELECTROVALVA, GPIO.HIGH)  # Turn off the electrovalve
        lcd.text("PUMP: OFF", 1)
        lcd.text("SOIL: WET", 2)
    else:
        GPIO.output(RELAY_PIN, GPIO.LOW)  # Turn on the pump
        GPIO.output(RELAY_PIN_ELECTROVALVA, GPIO.LOW)  # Turn on the electrovalve
       
 lcd.text("PUMP: ON", 1)
        lcd.text("SOIL: DRY", 2)
        sleep(5)  # Keep the pump on for 5 seconds
        GPIO.output(RELAY_PIN, GPIO.HIGH)  # Turn off the pump
        lcd.text("PUMP: OFF", 1)
        lcd.text("SOIL: DRY", 2)

@app.route('/')

def index():
    """Main page."""
    return render_template('index.html')

@app.route('/data')
def data():
    """Route for providing sensor data and generating real-time plot."""
    raw_value = adc.read_adc(3, gain=GAIN)  # Citirea valorii brute a ADC
    selected_plant = request.form.get('plant')  # Obține planta selectată din formular
    threshold = get_threshold_for_plant(selected_plant)
    activate_pump(raw_value, threshold)  # Activarea pompei în funcție de umiditatea solului

    # Generăm graficul în timp real
    x_data.append(len(x_data))  # Adăugăm o nouă valoare x (timp)
    y_data.append(raw_value)   # Adăugăm o nouă valoare y (valoare ADC)
    plt.plot(x_data, y_data, color='blue')  # Creăm graficul
    plt.xlabel('Time')
    plt.ylabel('Raw Value')
    plt.title('Real-time Raw Value Plot')
    plt.savefig('static/plot_temp1.png')  # Salvăm graficul ca fișier PNG
    #plt.savefig('/var/www/your_domain/login/plot_temp1.png')  # Salvăm graficul ca fișier PNG
    plt.clf()  # Curățăm figura pentru următorul grafic

    soil_status = wet_dry_level(raw_value, threshold)
    pump_status = "OFF" if GPIO.input(RELAY_PIN) else "ON"
    senzor_name = "Senzor De Umiditate 1"
    plants = get_plants()  # Obținem lista de plante din baza de date

    save_data_to_db(raw_value, soil_status, pump_status)

    return render_template('data.html', soil_status=soil_status, pump_status=pump_status, senzor_name=senzor_name, plants=plants, selected_plant=selected_plant)


@app.route('/select_plant', methods=['POST'])
def select_plant():
    if request.method == 'POST':
        selected_plant = request.form.get('plant')
        threshold = get_threshold_for_plant(selected_plant)
        # Actualizează pragul pentru noua plantă selectată
        # Apoi, reapelează funcția activate_pump() pentru a actualiza statusul pompei
        raw_value = adc.read_adc(3, gain=GAIN)  # Citește valoarea brută a ADC
        activate_pump(raw_value, threshold)
        # Redirecționează către pagina data.html, transmițând planta selectată înapoi la șablonul HTML
        return redirect(url_for('data', selected_plant=selected_plant))


def get_plants():
    """Funcție pentru a obține lista de plante din baza de date."""
    connection = pymysql.connect(host=mysql_host,
                                 user=mysql_user,
                                 password=mysql_password,
                                 db=mysql_db,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            # Selectăm toate plantele din tabela Plante
            sql = "SELECT nume_planta FROM Plante"
            cursor.execute(sql)
            plants = cursor.fetchall()
    finally:
        connection.close()
    return plants

def get_threshold_for_plant(plant_name):
    connection = pymysql.connect(host=mysql_host,
                                 user=mysql_user,
                                 password=mysql_password,
                                 db=mysql_db,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            # Selectează threshold-ul pentru planta selectată din tabela Plante
            sql = "SELECT threshold FROM Plante WHERE nume_planta = %s"
            cursor.execute(sql, (plant_name,))
            result = cursor.fetchone()
            if result:
                return result['threshold']
            else:
                return threshold  # Returnează THRESHOLD-ul implicit dacă nu există unul definit pentru planta
    finally:
        connection.close()


@app.route('/graph')
def graph():
    """Route for displaying the saved graph."""
    return render_template('graph.html')

def gen():
    """Video streaming generator function."""
    vs = cv2.VideoCapture(0)
    while True:
        ret, frame = vs.read()
        ret, jpeg = cv2.imencode('.jpg', frame)
        frame = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    """Video streaming route."""
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5003, debug=True, threaded=True)
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()
        lcd.clear()




