class load_cell:
    DAC_ADDR = 0x1f
    GPIO_ADDR = 0x40
    def __init__(self, bus):
        self.bus = bus
        self.bus.write_byte_data(load_cell.GPIO_ADDR, 0x04, 0x01)
        for reg in range(0x09, 0x10):
            self.bus.write_byte_data(load_cell.GPIO_ADDR, reg, 0x55)
        self.connected = True

    def set_dac_value(self, load_channel, value):
        if not (0 <= load_channel < 4):
            print 'Invalid channel number'
            return
        data = (value & 0x0000000F) << 12
        data |= (value & 0x00000FF0) >> 4
        self.bus.write_word_data(load_cell.DAC_ADDR, 0x30 + load_channel, data)

    def set_load_range(self, load_channel, rng):
        if not (0 <= load_channel < 4):
            print 'Invalid channel number'
            return
        elif rng not in [0.01, 0.1, 1, 10]:
            print 'Invalid range'
            return
        rng_idx = [10, 1, 0.1, 0.01].index(rng)
        if rng_idx == 0:
            data = 0x07
        elif rng_idx == 1:
            data = 0x0a
        elif rng_idx == 2:
            data = 0x11
        elif rng_idx == 3:
            data = 0x00
        if load_channel == 3 and rng == 0:
            print 'Channel does not support this range'
            return
        if load_channel == 0:
            self.bus.write_byte_data(load_cell.GPIO_ADDR, 0x41, data)
        elif load_channel == 1:
            self.bus.write_byte_data(load_cell.GPIO_ADDR, 0x49, data << 3)
        elif load_channel == 2:
            self.bus.write_byte_data(load_cell.GPIO_ADDR, 0x51, data << 3)
        elif load_channel == 3:
            self.bus.write_byte_data(load_cell.GPIO_ADDR, 0x59, data)
