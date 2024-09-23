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

        file = open(file, 'r')
        self.temp = file.read(-1).splitlines()
        file.close()
        
    def read_config(self):
        """
        Read config. Path should be sent as first argument
        :return: station_number, rest_api, use_itac, process_layer
        """
        try:
            for config_content in self.temp:
                match config_content.split('=')[0]:
                    case '##': continue
                    case 'stationNumber': self.station_number = config_content.split('=')[1]
                    case 'restAPI': self.rest_api = config_content.split('=')[1]
                    case 'ITAC': self.use_itac = config_content.split('=')[1]
                    case 'processLayer': self.process_layer = config_content.split('=')[1]

            return self.station_number, self.rest_api, bool(self.use_itac), self.process_layer
    
        except UnboundLocalError:
            windll.user32.MessageBoxW(0, 'Error 0x101 Variable not found in config.', 'Error', 0x1000)
            Logger.log_event(Logger(), 'Variable not found in config. ' + format_exc())
        except NameError:
            windll.user32.MessageBoxW(0, 'Error 0x102 Variable not found in return of function.', 'Error', 0x1000)
            Logger.log_event(Logger(), 'Variable not found in return of function. ' + format_exc())
