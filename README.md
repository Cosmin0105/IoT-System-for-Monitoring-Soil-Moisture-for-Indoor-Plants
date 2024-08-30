IoT-Based Soil Moisture Monitoring and Control System for Indoor Plants
Project Overview
This project implements an IoT-based system for monitoring soil moisture levels in indoor plants and controlling a water pump and electrovalve accordingly. The system uses a Raspberry Pi, ADC (Analog-to-Digital Converter), and sensors to collect real-time data on soil moisture. The data is processed to determine whether the soil is wet or dry, and based on the results, the system activates or deactivates the water pump and electrovalve to maintain optimal soil moisture levels.

The project also includes a web interface built with Flask that allows users to monitor the soil moisture data, view real-time plots, select plant types with specific soil moisture thresholds, and control the water pump manually if needed.

Key Features
Real-Time Soil Moisture Monitoring: The system continuously reads soil moisture data using an ADC and classifies it as "WET" or "DRY" based on a predefined threshold.

Automated Watering System: If the soil moisture level falls below the threshold (indicating "DRY"), the system automatically activates the water pump and electrovalve to irrigate the plant.

LCD Display: The status of the pump and soil moisture level is displayed on an LCD connected to the Raspberry Pi.

Web Interface: A Flask-based web application provides a user interface for monitoring real-time sensor data, viewing historical data, and manually selecting the plant type for threshold adjustment.

Data Logging: The system logs soil moisture readings, pump status, and other relevant data into a MySQL database, enabling historical analysis and reporting.

Real-Time Graphing: The system generates and displays real-time plots of soil moisture levels, allowing users to visualize changes over time.

Video Feed: The system includes an optional video streaming feature using a connected camera, providing live visuals of the plant.

Hardware Components

Raspberry Pi: The main processing unit for the system, running the Flask server and controlling sensors and actuators.

ADC (e.g., ADS1115): Converts the analog soil moisture sensor data to digital values that can be processed by the Raspberry Pi.

Soil Moisture Sensor: Detects the moisture level in the soil.

Water Pump & Electrovalve: Controlled via relay modules, used to water the plants when needed.

LCD Display: Displays the current status of the pump and soil moisture level.

Relay Modules: Control the operation of the water pump and electrovalve.

Camera Module (optional): Streams a live video feed of the plant area.

Software Components

Flask: A Python-based web framework used for developing the web interface.

RPi.GPIO: A Python library for controlling GPIO pins on the Raspberry Pi.

Adafruit_Python_ADS1x15: A Python library for interfacing with the ADS1115 ADC.

MySQL: Used for storing sensor data and plant information.

Matplotlib: Used for generating real-time plots of soil moisture data.

OpenCV: Used for capturing and streaming live video feed (optional).


Hardware Setup:

Connect the soil moisture sensor, ADC, relay modules, water pump, electrovalve, and LCD to the Raspberry Pi.

Optionally, connect a camera module for live video streaming.

![WhatsApp Image 2024-08-30 at 12 54 43_5d6ece2f](https://github.com/user-attachments/assets/3b2ff560-cac4-4092-9664-7aadcab8d46b)



Raspberry Pi 3B+

![raspppp](https://github.com/user-attachments/assets/8b51ba73-a90c-4c17-bb19-3bc6d65bfbb8)

Water Pump

![water_pump](https://github.com/user-attachments/assets/a91fe57b-1dd7-4b12-a0fa-fdaa35afef21)

ADC

![WhatsApp Image 2024-08-30 at 13 03 32_42e3f236](https://github.com/user-attachments/assets/e9f0c4ae-22df-45f1-9208-a1c50a526072)

Electrovalva

![electrovalvaa](https://github.com/user-attachments/assets/0e15adb1-0e29-4107-bd8d-815c47d35084)

LCD 

![lcds](https://github.com/user-attachments/assets/77090ee1-2ec2-481d-a7e5-2a1d0551b119)

ALL COMPONENTS 

![WhatsApp Image 2024-08-30 at 13 03 33_afd59280](https://github.com/user-attachments/assets/c380f2c0-5916-4a2b-a440-df7600857e8d)



Software Setup:

Install the necessary Python libraries:


pip install Flask rpi_lcd Adafruit_ADS1x15 RPi.GPIO matplotlib pymysql opencv-python



Set up the MySQL database with the required tables:


CREATE DATABASE login;

USE login;


-- Create 'users' table

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

-- Create 'SensorData' table

CREATE TABLE SensorData (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    raw_value INT NOT NULL,
    soil_status VARCHAR(10) NOT NULL,
    pump_status VARCHAR(3) NOT NULL
);

-- Create 'Plante' table

CREATE TABLE Plante (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nume_planta VARCHAR(100) NOT NULL,
    specie VARCHAR(100) NOT NULL,
    threshold INT NOT NULL
);



Interfaces:

![login](https://github.com/user-attachments/assets/1a73a9a5-f3db-4348-b9ec-a6c82b613a90)

![log2](https://github.com/user-attachments/assets/32654ff6-f8fd-40fc-8fb9-5035940cf0b8)

![pagprin](https://github.com/user-attachments/assets/603f3d89-8dea-4224-bae0-bdd9de11c0d2)

![1](https://github.com/user-attachments/assets/6c46c6dc-5201-4e56-b17b-e8585283ca49)


![222](https://github.com/user-attachments/assets/be6dc3a3-f676-4dde-af40-cf5a76dfaf8b)

![3333](https://github.com/user-attachments/assets/0dfaf5e1-738d-44b7-af9a-090a23d02b35)

![menu](https://github.com/user-attachments/assets/a21dfdcc-834a-4b6f-822c-a73f610bf56c)

![camera](https://github.com/user-attachments/assets/00c793de-99a8-4d30-9db3-bf481f3f9f9d)

![data1](https://github.com/user-attachments/assets/215c3292-0ce7-4e43-b732-61b278206888)

![data2](https://github.com/user-attachments/assets/66c25d9b-e534-4412-8521-d0c686808dd1)

![selectpalnt](https://github.com/user-attachments/assets/a044de23-c714-4874-8010-51fb8eadb57f)

![graph](https://github.com/user-attachments/assets/81f76a55-ef6e-41db-a381-2757603e8fe7)

![history](https://github.com/user-attachments/assets/2f7038a2-72c0-4d19-9bd8-06b1bb7c32dd)











