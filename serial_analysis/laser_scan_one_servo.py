import serial
import math
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import numpy as np

arduinoPort = "/dev/ttyACM0"
baudRate = 9600
serialPort = serial.Serial(arduinoPort, baudRate, timeout=1)
start_angle_1 = 90
start_angle_2 = 90

coordinates = []
angle_dists = []
while True:
    try:
        lineOfData = serialPort.readline().decode()
    except UnicodeDecodeError:
        continue
    if len(lineOfData) > 0:
        if "28528" in lineOfData:
            break
        try:
            analog_output = int(lineOfData.split(">")[-1].split()[2])
            # theta is pan_angle
            theta = int(lineOfData.split(">")[-1].split()[0])
            # phi is tilt_angle
            phi = int(lineOfData.split(">")[-1].split()[1])
        except IndexError:
            continue

        distance = 1.74133 * 0.995136**analog_output

        if distance < 0.1 or distance > 1.5:
            continue
        angle_dists.append([phi, distance])
        # Z is up, X is out of the sensor, Y is left of sensor
        x = (
            distance
            * math.cos(math.radians(start_angle_1 - theta))
            * math.sin(math.radians(start_angle_2 - phi))
        )
        y = (
            -distance
            * math.sin(math.radians(start_angle_1 - theta))
            * math.sin(math.radians(start_angle_2 - phi))
        )
        z = distance * math.cos(math.radians(start_angle_2 - phi))

        coordinates.append([x, y, z])

coordinates = np.array(coordinates)
fig = plt.figure()
ax = plt.axes(projection="3d")
ax.scatter3D(coordinates[:, 0], coordinates[:, 1], coordinates[:, 2])
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")
plt.show()
# angle_dists = np.array(angle_dists)
# plt.plot(angle_dists[:,0], angle_dists[:,1])
# plt.xlabel('Tilt Angle (Degrees)')
# plt.ylabel('Distance (m)')
# plt.title('Laser Scan (1 Servo)')
# plt.show()
