import serial
import time


class BandControl:
    def __init__(self):
        self.port = '/dev/ttyACM0'
        self.arduino = serial.Serial(self.port, 9600, timeout=1)
        time.sleep(2)

    def run(self):
        self.arduino.write(b'r')

    def pause(self):
        self.arduino.write(b'p')

    def stop(self):
        self.arduino.write(b's')
    
    def destroy(self):
        self.arduino.close()
