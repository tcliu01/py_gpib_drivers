import re

class regutils:
    def __init__(self, bus, slave_addr, regmap_path):
        self.bus = bus
        self.slave_addr = slave_addr
        self.registers = dict()
        self.bitfields = dict()
        f = open(regmap_path, 'r')
        lines = f.readlines()
        for line in lines:
            lst = line.split(',')
            addr = int(lst[4], 16)
            name = lst[5]
            if name in self.registers:
                print 'Error! Duplicate register name: ' + name
                return
            else:
                self.registers[name] = addr
            bits = lst[11:19]
            for i in range(8):
                match = re.match('(.+?)\[([0-9]+):([0-9]+)\]', bits[i])
                if match:
                    bitname = match.group(1)
                    high = int(match.group(2))
                    low = int(match.group(3))
                    width = high - low + 1
                    self.bitfields[bitname] = (name, (7 - i) - (width - 1), width)
                elif len(bits[i]) > 0:
                    self.bitfields[bits[i]] = (name, 7 - i, 1)

    @staticmethod
    def read_modify_write_byte(bus, addr, reg, offs, width, newval):
        val = bus.read_byte_data(addr, reg)
        modval = regutils.set_value(val, offs, width, newval)
        bus.write_byte_data(addr, reg, modval)
        
    @staticmethod
    def read_modify_write_byte_16b(bus, addr, reg, offs, width, newval):
        val = bus.read_byte_data_16b(addr, reg)
        modval = regutils.set_value(val, offs, width, newval)
        bus.write_byte_data_16b(addr, reg, modval)

    def read_register_16b(self, register_name):
        if register_name in self.registers:
            return bus.read_byte_data_16b(self.slave_addr,
                                          self.registers[register_name])
        else:
            print 'Error! No register with name: ' + register_name

    def write_register_16b(self, register_name, value):
        if register_name in self.registers:
            return bus.write_byte_data_16b(self.slave_addr,
                                           self.registers[register_name],
                                           value)
        else:
            print 'Error! No register with name: ' + register_name

    def read_bitfield_16b(self, bitfield_name):
        if bitfield_name in self.bitfields:
            (name, offs, width) = self.bitfields[bitfield_name]
            data = self.read_register_16b(name)
            mask = (1 << width) - 1
            data &= mask << offs
            data >>= offs
            return data
        else:
            print 'Error! No register with name: ' + register_name        

    def read_modify_write_bitfield_16b(self, bitfield_name, value):
        if bitfield_name in self.bitfields:
            (name, offs, width) = self.bitfields[bitfield_name]
            regutils.read_modify_write_byte_16b(self.bus, 
                                                self.slave_addr,
                                                self.registers[name],
                                                offs,
                                                width,
                                                value)
        else:
            print 'Error! No bitfield with name: ' + bitfield_name

    @staticmethod
    def set_value(val, offs, width, newval):
        mask = (1 << width) - 1
        val &= ~(mask << offs)
        val |= (newval & mask) << offs
        return val

    # for Raspberry pi
    @staticmethod
    def get_i2c_bus():
        f = open('/proc/cpuinfo', 'r')
        for l in f.readlines():
            match = re.match('Revision\t:\s1?0+([0-9a-f])', l)
            if match:
                rev = int(match.group(1), 16)
                if rev >= 0x2 and rev <= 0x3:
                    return 0
                elif rev >= 0x4 and rev <= 0xf:
                    return 1
                else:
                    return -1
        return -1
    
                
