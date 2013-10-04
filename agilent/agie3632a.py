import Gpib
import re

class agie3632a:
    def __init__(self, gpib_dev, gpib_addr, query_id = True, reset = True):
        self.connection = Gpib.Gpib(gpib_dev, gpib_addr)
        self.connected = True
        if query_id:
            self.connection.write('*IDN?')
            rdata = self.connection.read()
            if rdata.find('E3632A') == -1:
                self.connected = False
                print 'Instrument ID not correct'
        if reset:
            self.connection.write('*RST')
    
    def config(self, volt, curr):
        if self.connected == False:
            return
        else:
            wrstr = 'VOLT ' + str(volt) + ';CURR ' + str(curr) + ';'
            self.connection.write(wrstr)

    def enable_outputs(self, enabled):
        if self.connected == False:
            return
        else:
            wrstr = 'OUTP ' + ('ON' if enabled else 'OFF') 
            self.connection.write(wrstr)

    def beep(self, number):
        if self.connected == False:
            return
        else:
            for I in range(number):
                self.connection.write("syst:beep") #this is the beep command
