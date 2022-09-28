import math
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import numpy as np
from helper import *


def process_serial_input(serial_port):
    """
    This function listens to the serial port (object inputted to the function)
    and processes each line by converting the analog signal, pan angle, and
    tilt angle into a list of x, y, and z coordinates.
    """
    coordinates = []

    # While loop handles the listener on the serial port and terminates when
    # the 'stop' message is received
    while True:
        # Reading the serial port is nested into a try and except statement
        # to avoid fatal errors associated with decoding errors
        try:
            data = serial_port.readline().decode()
        except UnicodeDecodeError:
            continue
        if len(data) > 0:
            # If '28528' is received (which represents stop), stop execution of
            # the while loop
            if "28528" in data:
                break
            # Splitting the signal is nested in a try and except statement to
            # handle if the inputted signal is missing values
            try:
                # Infrared Sensor analog reading
                analog_output = int(data.split(">")[-1].split()[2])
                # Orientation of Pan Servo
                theta = int(data.split(">")[-1].split()[0])
                # Orientation of Tilt Servo
                phi = int(data.split(">")[-1].split()[1])
            except IndexError:
                continue

            # This converts the analog reading from the infrared sensor to the
            # estimated distance based on the computed calibration curve
            distance = 1.74133 * 0.995136**analog_output

            # This throws out distances outside of the expected operating range
            # of the infrared sensor
            if distance < 0.2 or distance > 1.5:
                continue

            # Converts distance, theta, phi into X, Y, Z coordinates using
            # equations that map spherical coordinates to cartesian coordiantes
            # The origin of this reference frame is the center of the infrared
            # sensor. Z is up, Y is out of the sensor, and X is left of sensor
            x = (
                distance
                * math.cos(math.radians(START_ANGLE - theta))
                * math.sin(math.radians(START_ANGLE - phi))
            )
            y = (
                distance
                * math.sin(math.radians(START_ANGLE - theta))
                * math.sin(math.radians(START_ANGLE - phi))
            )
            z = distance * math.cos(math.radians(START_ANGLE - phi))

            coordinates.append([x, y, z])
    return coordinates


def plot_scan(coordinates):
    """
    This function visualizes the results from the 3D scan. It takes in a 2D
    numpy array of X coordinates, Y coordinates, and Z coordinates.
    """
    ax = plt.axes(projection="3d")
    ax.scatter3D(coordinates[:, 0], coordinates[:, 1], coordinates[:, 2])

    # Sets axis titles for the plot
    ax.set_xlabel("X (meters)")
    ax.set_ylabel("Y (meters)")
    ax.set_zlabel("Z (meters)")
    ax.set_title("3D Scan")

    plt.show()


if __name__ == "__main__":
    serial_port = initialize_serial()
    coordinates = process_serial_input(serial_port)
    plot_scan(np.array(coordinates))
