#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick 
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
import socket


# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.


# Create your objects here.
ev3 = EV3Brick()

# Initialize a motor at port B.
test_motor = Motor(Port.D)
sensore = ColorSensor(Port.S1)

# Write your program here

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
