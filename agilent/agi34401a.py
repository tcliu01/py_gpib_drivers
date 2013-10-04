import Gpib
import re

class agi34401a:
    def __init__(self, gpib_dev, gpib_addr, query_id = True, reset = True):
        self.connection = Gpib.Gpib(gpib_dev, gpib_addr)
        self.connected = True
        if query_id:
            self.connection.write('*IDN?')
            rdata = self.connection.read()
            if rdata.find('34401A') == -1:
                self.connected = False
                print 'Instrument ID not correct'
        if reset:
            self.connection.write('*RST')

    def min_greater_than(self, num_list, min_case, max_case, value):
        if value <= num_list[0]:
            return min_case
        elif value > num_list[-1]:
            return max_case
        else:
            for i in range(len(num_list) - 1):
                if value > num_list[i] and value <= num_list[i + 1]:
                    return num_list[i + 1]
            
    def config_vdc(self, auto_rng=True, rng=1.0, res=5.5, nplc=10, man_rng_plc=False):
        # decode PLC
        num_plc = [0.02, 0.06, 0.2, 1, 10, 100]
        nplc = self.min_greater_than(num_plc, num_plc[0], num_plc[-1], nplc)
        # auto range
        if auto_rng:
            wrstr = 'FUNC "VOLT:DC";:VOLT:DC:RANGE:AUTO ON;:VOLT:DC:NPLC ' + str(nplc)
        # not auto range
        else:
            wrstr = 'FUNC "VOLT:DC";:VOLT:DC:RANGE '
            num_rng = [0.1, 1.0, 10.0, 100.0, 1000.0]
            rng = self.min_greater_than(num_rng, num_rng[0], num_rng[-1], rng)
            wrstr += str(rng)
            # use nplc for manual range
            if man_rng_plc:
                wrstr += ';:VOLT:DC:NPLC ' + str(nplc)
            # use resolution for manual range
            else:
                wrstr += ';:VOLT:DC:RES '
                num_res = [4.5, 5.5, 6.5]
                mult_res = [1e-4, 1e-5, 1e-6, 3e-7]
                res = int(self.min_greater_than(num_res, num_res[0], num_res[-1] + 1, res) - num_res[0])
                wrstr += str(mult_res[res] * rng)
        self.connection.write(wrstr)

    def config_adc(self, auto_rng=True, nplc=10, rng=1.0, res=5.5, man_rng_plc=False):
        # decode PLC
        num_plc = [0.02, 0.06, 0.2, 1, 10, 100]
        nplc = self.min_greater_than(num_plc, num_plc[0], num_plc[-1], nplc)
        # auto range
        if auto_rng:
            wrstr = 'FUNC "CURR:DC";:CURR:DC:RANGE:AUTO ON;:CURR:DC:NPLC ' + str(nplc)
        # not auto range
        else:
            wrstr = 'FUNC "CURR:DC";:CURR:DC:RANGE '
            num_rng = [0.01, 0.1, 1.0, 3.0]
            rng = self.min_greater_than(num_rng, num_rng[0], num_rng[-1], rng)
            wrstr += str(rng)
            # use nplc for manual range
            if man_rng_plc:
                wrstr += ';:CURR:DC:NPLC ' + str(nplc)
            # use resolution for manual range
            else:
                wrstr += ';:CURR:DC:RES '
                num_res = [4.5, 5.5, 6.5]
                mult_res = [1e-4, 1e-5, 1e-6, 3e-7]
                res = int(self.min_greater_than(num_res, num_res[0], num_res[-1] + 1, res) - num_res[0])
                wrstr += str(mult_res[res] * rng)
        self.connection.write(wrstr)

    def read(self):
        if self.connected == False:
            return
        self.connection.write('TRIG:SOUR IMM;:TRIG:COUN 1.00E+0;:INIT')
        self.connection.write('*OPC?')
        self.connection.read()
        self.connection.write('FETCH?')
        data = self.connection.read()
        return float(data)

    def beep(self, number):
        if self.connected == False:
            return
        else:
            for I in range(number):
                self.connection.write("syst:beep") #this is the beep command
