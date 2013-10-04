import Gpib
import re

class agi34970a:
    def __init__(self, gpib_dev, gpib_addr, query_id = True, reset = True):
        self.connection = Gpib.Gpib(gpib_dev, gpib_addr)
        self.connected = True
        if query_id:
            self.connection.write('*IDN?')
            rdata = self.connection.read()
            if rdata.find('34970A') == -1 and rdata.find('34972A') == -1:
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
    
    def config_vdc(self, channels, auto_imp = False, nplc = 1, auto_rng = True, rng = 1000):
        if len(channels) == 0 or self.connected == False:
            return
        else:
            chstr = self.channels(channels)
            wrstr = 'SENS:FUNC "VOLT:DC", ' + chstr + ';'
            wrstr += ':INP:IMP:AUTO ' + ('ON' if auto_imp else 'OFF') + ', ' + chstr + ';'
            wrstr += ':SENS:VOLT:DC:NPLC '
            num_nplc = [0.02, 0.2, 1, 2, 10, 20, 100, 200]
            str_nplc = ['.02', '.2', '1', '2', '10', '20', '100', '200']
            if nplc <= 0.02:
                wrstr += '.02'
            elif nplc > 200:
                wrstr += 'MAX'
            else:
                for i in range(len(num_nplc) - 1):
                    if nplc > num_nplc[i] and nplc <= num_nplc[i + 1]:
                        wrstr += str_nplc[i + 1]
                        break
            wrstr += ', ' + chstr + ';'
            wrstr += ':SENS:VOLT:DC:RANG:AUTO '
            wrstr += ('ON' if auto_rng else 'OFF') + ', ' + chstr + ';'
            if not auto_rng:
                wrstr += ':SENS:VOLT:DC:RANG '
                num_rng = [0.1, 1, 10, 100, 300]
                str_rng = ['0.1', '1', '10', '100', '300']
                if rng <= 0.1:
                    wrstr += '0.1'
                elif rng > 300:
                    wrstr += 'MAX'
                else:
                    for i in range(len(num_rng) - 1):
                        if rng > num_rng[i] and rng <= num_rng[i + 1]:
                            wrstr += str_rng[i + 1]
                            break
                wrstr += ', ' + chstr + ';'
            self.connection.write(wrstr)

    def config_scan(self, channels):
        if len(channels) == 0 or self.connected == False:
            return
        else:
            wrstr = 'ROUT:SCAN ' + self.channels(channels)
            self.connection.write(wrstr)

    def read(self):
        if self.connected == False:
            return
        self.connection.write('TRIG:SOUR IMM;:TRIG:TIM MIN;:TRIG:COUNT 1.00E+0;:INIT')
        self.connection.write('*OPC?')
        self.connection.read()
        self.connection.write('DATA:POIN?')
        num_points = int(self.connection.read())
        if num_points > 0:
            self.connection.write('DATA:REM? ' + str(num_points))
            data = (self.connection.read()).split(',')
            for i in range(len(data)):
                data[i] = float(data[i])
            return data

    def beep(self, number):
        if self.connected == False:
            return
        else:
            for I in range(number):
                self.connection.write("syst:beep") #this is the beep command
