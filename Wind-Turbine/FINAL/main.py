#!/usr/bin/env pybricks-micropython
from pybricks import ev3brick as brick
from pybricks.ev3devices import Motor, ColorSensor
from pybricks.parameters import Port, Button, Color
from pybricks.tools import wait
import socket
import _thread  # Importa il modulo per i thread

# Funzione per gestire la ricezione dei dati dal client
def receive_data(client, start_acquisition):
    while True:
        try:
            # Attendi i dati dal client (questa operazione è bloccante, ma è gestita in un thread separato)
            data = client.recv(1024).decode('utf-8')
            
            if data == "START_MOTOR":
                start_acquisition[0] = True
                brick.display.text("Inizio acquisizione")
            elif data == "STOP_MOTOR":
                start_acquisition[0] = False
                brick.display.text("Acquisizione interrotta")
            elif data == "STOP":
                brick.display.clear()
                motore.stop()
                client.close()
                server.close()
                
        except Exception as e:
            brick.display.text("Errore Ricezione")
            break

# Funzione principale
def main():
    # Inizializzazione
    brick.display.clear()
    brick.display.text("Avvio...")
   
    # Setup dispositivi
    motore = Motor(Port.A)
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

    start_acquisition = [False]  # Usato come lista per riferimenti mutabili tra thread
   
    try:
        # Avvio del thread per la ricezione dei dati
        _thread.start_new_thread(receive_data, (client, start_acquisition))

        while True:
            if start_acquisition[0]:
                # Lettura e invio speed
                speed = motore.speed()
                speed_str = str(speed)
                
                try:
                    client.send(speed_str.encode())
                except Exception as e:
                    brick.display.text(str(e))
                
            wait(1000)
   
    except Exception as e:
        brick.display.text("Errore")
       
    finally:
        motore.stop()
        client.close()
        server.close()

if __name__ == "__main__":
    main()
