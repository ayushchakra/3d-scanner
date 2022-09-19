import serial

arduinoPort = '/dev/ttyACM0'
baudRate = 9600
serialPort = serial.Serial(arduinoPort, baudRate, timeout=1)
while True:
    lineOfData = serialPort.readline().decode()
    if len(lineOfData) > 0:
        print(lineOfData.split('>')[-1])
        # print("a = " + str(a), end="")
        # print(", b = " + str(b), end="")
        # print(", c = " + str(c), end="")
        # print(", d = " + str(d))
serialPort.close()
exit()