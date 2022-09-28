import serial


def initialize_serial():
    """
    This function intitializes the serial connection to the arduino and returns
    a serial object that can be used to read serial messages.
    """
    # USB port that is connected to the Arduino
    arduino_port = "/dev/ttyACM0"
    # Sets the Baud Rate of the expected serial input
    baud_rate = 9600
    # Establishes the connected to the serial port
    serialPort = serial.Serial(arduino_port, baud_rate, timeout=1)
    return serialPort


START_ANGLE = 90
