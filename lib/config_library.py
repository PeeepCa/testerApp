from ctypes import windll
from traceback import format_exc

from lib.logger_library import Logger


class Config:
    """
    Read config. Path should be sent as first argument.
    :param file: Config file to read.
    """
    def __init__(self, file):
        self.station_number = None
        self.rest_api = None
        self.use_itac = None
        self.process_layer = None
        self.use_reader = None
        self.reader_com = None
        self.reader_baud = None
        self.reader_bytesize = None
        self.reader_parity = None
        self.reader_stopbits = None
        self.reader_timeout = None

        file = open(file, 'r')
        self.temp = file.read(-1).splitlines()
        file.close()
        
    def read_config(self):
        """
        Read config. Path should be sent as first argument
        :return: station_number, rest_api, use_itac, process_layer, use_reader, reader_com, reader_baud, reader_bytesize, reader_parity, reader_stopbits, reader_timeout
        """
        try:
            for config_content in self.temp:
                match config_content.split('=')[0]:
                    case '##': continue
                    case 'stationNumber': self.station_number = config_content.split('=')[1]
                    case 'restApi': self.rest_api = config_content.split('=')[1]
                    case 'Itac':
                        self.use_itac = config_content.split('=')[1]
                        if self.use_itac == 'True': self.use_itac = True
                    case 'processLayer': self.process_layer = config_content.split('=')[1]
                    case 'useReader':
                        self.use_reader = config_content.split('=')[1]
                        if self.use_reader == 'True': self.use_reader = True
                    case 'readerCom': self.reader_com = config_content.split('=')[1]
                    case 'readerBaud': self.reader_baud = config_content.split('=')[1]
                    case 'readerTimeout': self.reader_timeout = config_content.split('=')[1]
                    case 'readerBytesize': self.reader_bytesize = config_content.split('=')[1]
                    case 'readerParity': self.reader_parity = config_content.split('=')[1]
                    case 'readerStopbits': self.reader_stopbits = config_content.split('=')[1]
                    case 'readerTimeout': self.reader_timeout = config_content.split('=')[1]

            return self.station_number, self.rest_api, self.use_itac, self.process_layer, self.use_reader, self.reader_com, int(self.reader_baud), int(self.reader_bytesize), self.reader_parity, int(self.reader_stopbits), int(self.reader_timeout)
    
        except UnboundLocalError:
            windll.user32.MessageBoxW(0, 'Error 0x101 Variable not found in config.', 'Error', 0x1000)
            Logger.log_event(Logger(), 'Variable not found in config. ' + format_exc())
        except NameError:
            windll.user32.MessageBoxW(0, 'Error 0x102 Variable not found in return of function.', 'Error', 0x1000)
            Logger.log_event(Logger(), 'Variable not found in return of function. ' + format_exc())
