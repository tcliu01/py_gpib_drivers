import Gpib
import re

class delta901x:
    def __init__(self, gpib_dev, gpib_addr, reset=True):
        self.connection = Gpib.Gpib(gpib_dev, gpib_addr)
        self.connected = True
        if reset:
            self.connection.write('N C')
            
    def config_heat(self, heat):
        if self.connected == False:
            return
        else:
            wrstr = 'H ' + ('ON' if heat else 'OF')
            self.connection.write(wrstr)

    def config_cool(self, cool):
        if self.connected == False:
            return
        else:
            wrstr = 'C ' + ('ON' if cool else 'OF')
            self.connection.write(wrstr)

    def config_temp(self, temp):
        if self.connected == False:
            return
        else:
            wrstr = 'SET ' + "%.1f" % temp
            self.connection.write(wrstr)
