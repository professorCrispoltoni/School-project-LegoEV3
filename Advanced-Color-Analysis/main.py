#!/usr/bin/env pybricks-micropython
from pybricks import ev3brick as brick
from pybricks.ev3devices import Motor, ColorSensor
from pybricks.parameters import Port, Button, Color
from pybricks.tools import wait
import socket

def main():
    # Inizializzazione
    brick.display.clear()
    brick.display.text("Avvio...")
    
    # Setup dispositivi
    motore = Motor(Port.D)
    sensore = ColorSensor(Port.S1)
    
    # Imposta velocità iniziale a 0
    motore.stop()  # Assicurarsi che il motore sia fermo all'avvio
    
    # Setup server
    server = socket.socket()
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('', 12345))
    server.listen(1)
    
    brick.display.text("Attesa client...")
    client, _ = server.accept()
    brick.display.text("Connesso!")
    
    # Avvio motore
    # Inizialmente, il motore è fermo
    motore.stop()
    
    try:
        while True:
               
            # Lettura e invio colore
            colore = sensore.color()
            colore_str = {
                Color.RED: 'ROSSO', Color.GREEN: 'VERDE',
                Color.BLUE: 'BLU', Color.YELLOW: 'GIALLO',
                Color.BLACK: 'NERO', Color.WHITE: 'BIANCO'
            }.get(colore)
            
            if colore_str:
                try:
                    client.send(colore_str.encode())
                    brick.display.text(colore_str)
                except Exception as e:
                    print(str(e))
                    break
                    
            # Gestione dei comandi ricevuti
            data = client.recv(1024).decode('utf-8')
            if data == "START_MOTOR":
                motore.run(200)  # Imposta la velocità a 200
                brick.display.text("Motori Avviati")
            elif data == "STOP_MOTOR":
                motore.stop()  # Ferma il motore
                brick.display.text("Motori Fermati")
                    
            wait(1000)
            
    except Exception as e:
        brick.display.text("Errore")
        
    finally:
        motore.stop()
        client.close()
        server.close()

if __name__ == "__main__":
    main()
