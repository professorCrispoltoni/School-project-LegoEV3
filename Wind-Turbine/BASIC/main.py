#!/usr/bin/env pybricks-micropython
from pybricks import ev3brick as brick
from pybricks.hubs import EV3Brick 
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
import socket

import threading

# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.


# Create your objects here.
ev3 = EV3Brick()

# Initialize a motor at port B.
test_motor = Motor(Port.D)
sensore = ColorSensor(Port.S1)

# Write your program here

HOST = "127.0.0.1"  # Ascolta solo sulla macchina locale
PORT = 12345  # Porta per la connessione

# Simulated state variables
motor_running = False
motor_speed = 0

def stampaInfo(msg):
    brick.display.text(msg)

def handle_client(client_socket):
    global motor_running, motor_speed
    try:
        while True:
            # Ricevi comandi dal client
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break

            #print(f"Comando ricevuto: {data}")
            stampaInfo("Comando ricevuto:"+str(data))

            # Risposta ai comandi
            if data == "START_MOTOR":
                motor_running = True
                test_motor.run_target(500, 90)
                response = "MOTOR_STARTED"
            elif data == "STOP_MOTOR":
                motor_running = False
                response = "MOTOR_STOPPED"
            elif data.startswith("SET_SPEED:"):
                motor_speed = int(data.split(":")[1])
                #response = f"SPEED_SET:{motor_speed}"
                response = "SPEED_SET:"+str(motor_speed)

            elif data == "GET_SENSOR_DATA":
                # Simula un colore casuale
                simulated_color = random.choice(["Red", "Green", "Blue", "Yellow", "White", "Black"])
                #response = f"SENSOR_DATA:{simulated_color}"
                response = "SENSOR_DATA:"+str(simulated_color)
            else:
                response = "UNKNOWN_COMMAND"

            # Invia la risposta al client
            client_socket.sendall(response.encode('utf-8'))

    except Exception as e:
        #print(f"Errore durante la comunicazione con il client: {e}")
        stampaInfo("Errore : "+str(e))
       
    finally:
        stampaInfo("Client disconnesso.")
        client_socket.close()

def start_server():
    #socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server
    server = socket.socket()
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('', PORT))
    server.listen(1)
    #print(f"Server  in ascolto su {'169.254.120.34'}:{PORT}...")
    stampaInfo("Server  in ascolto....")

    while True:
        client_socket, addr = server.accept()
        #print(f"Connessione stabilita con {addr}")
        stampaInfo("Connessione stabilita")
        threading.Thread(name="pluto",target=handle_client, args=(client_socket,)).start()

def setupBrick():
    brick.display.clear()
    brick.display.text("avvio server...")

if __name__ == "__main__":
    setupBrick()
    start_server()


'''
# Play a sound.
for i in range(0,2):
    ev3.speaker.beep()
    wait(1000)

# Run the motor up to 500 degrees per second. To a target angle of 90 degrees.
test_motor.run_target(500, 90)

# Play another beep sound.
ev3.speaker.beep(frequency=1000, duration=500)

#lettura e invio colore
colore = sensore.color()
colore_str = {
    Color.RED: 'ROSSO', Color.GREEN: 'VERDE', Color.BLUE: 'BLU', Color.YELLOW: 'GIALLO', Color.BLACK: 'NERO', Color.WHITE: 'BIANCO'
}.get(colore)

print(colore_str)
'''