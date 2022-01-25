"""
This class enables the serial connection between arduino and python
"""

import serial


class SerialArduino:

    def __init__(self):
        # identification letters for classifying the data
        self.identification = ['A', 'B', 'C']
        # serial port
        self.arduinoSerial = serial.Serial(port='/dev/tty.usbmodem1101', baudrate=9600)
        self.arduinoSerial.timeout = 1

        # list for the valid data
        self.data_l = [0, 0, 0]
        # list for the old data
        self.data_l_old = [0, 0, 0]

        # counter to keep track of how often states area changed
        self.counter_one = 0

    # this method reads the data input and returns that to the classifying method
    def read_input(self):
        dataSerial = self.arduinoSerial.readline().decode('ascii').rstrip() # rstrip() removes line breaks in the data
        return dataSerial

    def classify_data(self, data):

        # checking if the data is not empty
        if len(data) > 0:
            identifier = data[0]

            # checking for every identifier if it is at the start of the data
            if identifier == 'A':
                # if the identifier is valid, the rest of the data (without the identifier) gets saved into the data_
                # list
                self.data_l[0] = int(data[1:])
                self.data_l[2] = 0
            else:
                pass
            if identifier == 'B':
                self.data_l[1] = int(data[1:])
                self.data_l[2] = 0
            else:
                pass
            if identifier == 'C':
                # data from 'C' has to be carefully used. a double input is fatal. Keeping track of states with
                # "old_values" makes it possible to control game action
                if int(self.data_l_old[2]) == 0:
                    self.data_l[2] = int(data[1:])
                else:
                    # giving the program time to change states back to "normal" data in 10 rounds
                    if self.counter_one < 10:  #counter for stop bug where button press sended more then 1 time when pressed
                        self.counter_one += 1
                        self.data_l[2] = 0
                    else:
                        self.data_l[2] = int(data[1:])
                        self.counter_one = 0
                # updating the old data
                self.data_l_old[2] = self.data_l[2]
            else:
                # if there is data that is neither 'A', 'B' or 'C' then do nothing
                pass
                # print("Unclassifiable data")
