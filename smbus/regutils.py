import re

class regutils:
    @staticmethod
    def read_modify_write_byte(bus, addr, reg, offs, width, newval):
        val = bus.read_byte_data(addr, reg)
        modval = regutils.set_value(val, offs, width, newval)
        bus.write_byte_data(addr, reg, modval)

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
    
                
