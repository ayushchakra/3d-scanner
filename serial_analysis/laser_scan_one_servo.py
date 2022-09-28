from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import numpy as np
from helper import initialize_serial


def process_serial_input(serial_port):
    """
    This function listens to the serial port (object inputted to the function)
    and processes each analog reading into a distance using the calculated
    calibration curve. This function returns angle distance pairs as a 2D list.
    """
    angle_dists = []

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

            # This throws out distances outside of the expected operating range
            # of the infrared sensor
            distance = 1.74133 * 0.995136**analog_output

            if distance < 0.1 or distance > 1.5:
                continue

            # phi can be changed with theta to analyze tilt vs. distance
            angle_dists.append([phi, distance])
    return angle_dists


def plot_scan(angle_dists):
    """
    This function visualizes the angle distance pairs form the one servo sweep.
    It takes in a 2D array of angles and distances.
    """
    plt.plot(angle_dists[:, 0], angle_dists[:, 1])

    # Sets axis titles for the plot
    plt.xlabel("Tilt Angle (Degrees)")
    plt.ylabel("Distance (m)")
    plt.title("Laser Scan (1 Servo)")

    plt.show()


if __name__ == "__main__":
    serial_port = initialize_serial()
    angle_dists = process_serial_input(serial_port)
    plot_scan(np.array(angle_dists))
