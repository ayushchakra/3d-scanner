import serial
import math
import matplotlib.pyplot as plt
import numpy as np

arduinoPort = '/dev/ttyACM0'
baudRate = 9600
serialPort = serial.Serial(arduinoPort, baudRate, timeout=1)
start_angle_1 = 90
start_angle_2 = 90

coordinates = []
while True:
    lineOfData = serialPort.readline().decode()
    if len(lineOfData) > 0:
        if lineOfData == 'stop':
            break
        analog_output = lineOfData.split('>')[-1].split()[1]
        theta = lineOfData.split('>')[-1].split()[3]
        phi = lineOfData.split('>')[-1].split()[5]
        
        distance = 1.74133 * 0.995136**analog_output
        if distance < .1 or distance > 1.5:
            continue
        # Z is up, X is out of the sensor, Y is left of sensor
        x = distance*math.cos(math.radians(start_angle_1-theta))*math.sin(math.radians(start_angle_2-phi))
        y = distance*math.sin(math.radians(start_angle_1-theta))*math.sin(math.radians(start_angle_2-phi))
        z = distance*math.cos(math.radians(start_angle_2-phi))
        
        coordinates.append([x, y, z])
coordinates = np.array(coordinates)
plt.plot(coordinates[:,0], coordinates[:,1], coordinates[:,2])