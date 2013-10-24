import math
import bisect
import urllib2

class tds3000b:
    TRIGGER_EDGE_FALLING=0
    TRIGGER_EDGE_RISING=1
    TRIGGER_MODE_AUTO=0
    TRIGGER_MODE_NORMAL=1
    PERSISTENCE_MINIMUM=0
    PERSISTENCE_AUTO=-1
    PERSISTENCE_INFINITE=-2

    def __init__(self, ip_addr):
        self.image_addr = 'http://' + ip_addr + '/image.png'
        self.control_addr = 'http://' + ip_addr + '/?COMMAND=:'
        
    def fetch_image(self, filename=None):
        conn = urllib2.urlopen(self.image_addr)
        if not filename:
            return conn.read()
        else:
            f = open(filename, 'wb')
            f.write(conn.read())
            f.close()

    def pass_message(self, scpi_cmds, scpi_args=None, response=False):
        if not scpi_args:
            req_string = self.control_addr + scpi_cmds
        else:
            req_string = '+'.join([self.control_addr + scpi_cmds, scpi_args])
        conn = urllib2.urlopen(req_string)
        if response:
            return conn.read().strip()

    def single_seq(self):
        self.pass_message('ACQ:STOPA', 'SEQ')

    def run_stop(self, run):
        self.pass_message('ACQ:STOPA', 'RUNST')
        if run:
            self.pass_message('ACQ:STATE', 'RUN')
        else:
            self.pass_message('ACQ:STATE', 'STOP')

    def set_persistence(self, persistence):
        if persistence == tds3000b.PERSISTENCE_AUTO:
            self.pass_message('DIS:PERS', 'AUTO')
        elif persistence == tds3000b.PERSISTENCE_INFINITE:
            self.pass_message('DIS:PERS', 'INFI')
        elif persistence == tds3000b.PERSISTENCE_MINIMUM:
            self.pass_message('DIS:PERS', 'MINI')
        else:
            self.pass_message('DIS:PERS', str(persistence))

    def clear_persistence(self):
        self.pass_message('DIS:PERS:CLEAR')

    @staticmethod
    def make_scale_nice(raw_value):
        scale_list = [1.0, 2.0, 5.0, 10.0]
        (mantissa, exponent) = math.modf(math.log10(raw_value))
        if mantissa < 0:
            mantissa = math.pow(10, mantissa) * 10
            exponent -= 1
        else:
            mantissa = math.pow(10, mantissa)
        insert_point = bisect.bisect_right(scale_list, mantissa)
        err_up = scale_list[insert_point] - mantissa
        err_down = mantissa - scale_list[insert_point - 1]
        if err_up > err_down:
            new_mantissa = scale_list[insert_point - 1]
        else:
            new_mantissa = scale_list[insert_point]
        return new_mantissa * math.pow(10, exponent)

    def set_vertical_scale(self, channel, scale):
        scpi_cmds = 'CH' + str(channel) + ':SCA'
        scpi_args = str(scale)
        self.pass_message(scpi_cmds, scpi_args)

    def set_horizontal_scale(self, scale):
        self.pass_message('HOR:SCA', str(scale))
        
    def get_horizontal_scale(self):
        return float(self.pass_message('HOR:SCA?', response=True))

    def configure_trigger_a_edge(self, source, slope, level, mode):
        self.pass_message('TRIG:A:TYP', 'EDG')
        self.pass_message('TRIG:A:EDG:SOU', 'CH' + str(source))
        if slope == tds3000b.TRIGGER_EDGE_FALLING:
            self.pass_message('TRIG:A:EDG:SLO', 'FALL')
        else:
            self.pass_message('TRIG:A:EDG:SLO', 'RIS')
        self.pass_message('TRIG:A:LEV', str(level))
        if mode == tds3000b.TRIGGER_MODE_AUTO:
            self.pass_message('TRIG:A:MOD', 'AUTO')
        else:
            self.pass_message('TRIG:A:MOD', 'NORM')

    def get_measurement(self, channel, measurement):
        self.pass_message('MEASU:IMM:SOURCE', 'CH' + str(channel))
        self.pass_message('MEASU:IMM:TYP', measurement)
        result = self.pass_message('MEASU:IMM:VAL?', response=True)
        units = self.pass_message('MEASU:IMM:UNI?', response=True)
        return (float(result), units.strip('"'))
        
