import Gpib
import re

class agie3631a:
    def __init__(self, gpib_dev, gpib_addr, query_id = True, reset = True):
        self.connection = Gpib.Gpib(gpib_dev, gpib_addr)
        self.connected = True
        if query_id:
            self.connection.write('*IDN?')
            rdata = self.connection.read()
            if rdata.find('E3631A') == -1 and rdata.find('E3632A') == -1:
                self.connected = False
                print 'Instrument ID not correct'
        if reset:
            self.connection.write('*RST')
            
    def channels(self, channels):
        cstr = '(@'
        l = len(channels)
        for i in range(l):
            cstr += str(channels[i])
            if i == (l - 1):
                cstr += ')'
            else:
                cstr += ','
        return cstr
    
    def config_p6v(self, volt, curr):
        if self.connected == False:
            return
        else:
            wrstr = ':INST P6V;:VOLT ' + str(volt) + ';:CURR ' + str(curr) + ';'
            self.connection.write(wrstr)

    def config_p25v(self, volt, curr):
        if self.connected == False:
            return
        else:
            wrstr = ':INST P25V;:VOLT ' + str(volt) + ';:CURR ' + str(curr) + ';'
            self.connection.write(wrstr)

    def config_n25v(self, volt, curr):
        if self.connected == False:
            return
        else:
            wrstr = ':INST N25V;:VOLT ' + str(volt) + ';:CURR ' + str(curr) + ';'
            self.connection.write(wrstr)

    def enable_outputs(self, enabled):
        if self.connected == False:
            return
        else:
            wrstr = 'OUTP:STAT ' + ('ON' if enabled else 'OFF') 
            self.connection.write(wrstr)

    def meas_voltage_p6v(self):
        if self.connected == False:
            return
        else:
            self.connection.write('MEAS:VOLT? P6V')
            return float(self.connection.read())

    def meas_voltage_p25v(self):
        if self.connected == False:
            return
        else:
            self.connection.write('MEAS:VOLT? P25V')
            return float(self.connection.read())

    def meas_voltage_n25v(self):
        if self.connected == False:
            return
        else:
            self.connection.write('MEAS:VOLT? N25V')
            return float(self.connection.read())


    def meas_current_p6v(self):
        if self.connected == False:
            return
        else:
            self.connection.write('MEAS:CURR? P6V')
            return float(self.connection.read())

    def meas_current_p25v(self):
        if self.connected == False:
            return
        else:
            self.connection.write('MEAS:CURR? P25V')
            return float(self.connection.read())

    def meas_current_n25v(self):
        if self.connected == False:
            return
        else:
            self.connection.write('MEAS:CURR? N25V')
            return float(self.connection.read())

    def beep(self, number):
        if self.connected == False:
            return
        else:
            for I in range(number):
                self.connection.write("syst:beep") #this is the beep command
