import lib.shared_variables

from lib.logger_library import Logger
from traceback import format_exc
from lib.rs232_library import Rs232
from time import sleep


class Sequence:
    """
    Calling the sequence file to process it.
    :param file: path to the sequence file
    """
    def __init__(self, file, thread_number):
        self.settings_start = None
        self.settings_end = None
        self.thread_number = thread_number
        self.station_number = None
        self.process_layer = None
        self.restApi = None

        file = open(file, 'r')
        self.sequence_file = file.read(-1).splitlines()
        file.close()

        size = len(self.sequence_file)

        for settings_size in range(size):
            if '[SETTINGS]' in self.sequence_file[settings_size]:
                self.settings_start = settings_size
            elif '[SETTINGS_END]' in self.sequence_file[settings_size]:
                self.settings_end = settings_size
                break

        for preuut_size in range(size):
            if '[PREUUT]' in self.sequence_file[preuut_size]:
                self.preuut_start = preuut_size
            elif '[PREUUT_END]' in self.sequence_file[preuut_size]:
                self.preuut_end = preuut_size
                break

        for sequence_size in range(size):
            if '[SEQUENCE]' in self.sequence_file[sequence_size]:
                self.sequence_start = sequence_size
            elif '[SEQUENCE_END]' in self.sequence_file[sequence_size]:
                self.sequence_end = sequence_size
                break

        for postuut_size in range(size):
            if '[PREUUT]' in self.sequence_file[postuut_size]:
                self.postuut_start = postuut_size
            elif '[PREUUT_END]' in self.sequence_file[postuut_size]:
                self.postuut_end = postuut_size
                break

    def settings_read(self):
        """
        Read settings from config file.
        """
        try:
            for i in range(self.settings_start + 1, self.settings_end):
                if '##' in self.sequence_file[i]:
                    continue
                if ',,,' in self.sequence_file[i]:
                    continue
                match self.sequence_file[i].split(',')[1]:
                    case 'stationNumber':
                        self.station_number = self.sequence_file[i].split(',')[3]
                    case 'processLayer':
                        self.process_layer = self.sequence_file[i].split(',')[3]
                    case 'restApi':
                        self.restApi = self.sequence_file[i].split(',')[3]
                    case 'serialCom':
                        globals()[str(self.sequence_file[i].split(',')[1] +
                                      self.sequence_file[i].split(',')[2])] = self.sequence_file[i].split(',')[3]
                    case 'serialBaud':
                        globals()[str(self.sequence_file[i].split(',')[1] +
                                      self.sequence_file[i].split(',')[2])] = self.sequence_file[i].split(',')[3]
                    case 'serialBytesize':
                        globals()[str(self.sequence_file[i].split(',')[1] +
                                      self.sequence_file[i].split(',')[2])] = self.sequence_file[i].split(',')[3]
                    case 'serialParity':
                        globals()[str(self.sequence_file[i].split(',')[1] +
                                      self.sequence_file[i].split(',')[2])] = self.sequence_file[i].split(',')[3]
                    case 'serialStopbits':
                        globals()[str(self.sequence_file[i].split(',')[1] +
                                      self.sequence_file[i].split(',')[2])] = self.sequence_file[i].split(',')[3]
                    case 'serialTimeout':
                        globals()[str(self.sequence_file[i].split(',')[1] +
                                      self.sequence_file[i].split(',')[2])] = self.sequence_file[i].split(',')[3]
                    case _:
                        pass
        except (Exception, BaseException):
            print('Error 0x200 Undefined error in sequence call. ' + format_exc())
            Logger.log_event(Logger(), 'Error 0x200 Undefined error in sequence call. ' + format_exc())

    def preuut_read(self):
        """
        Read preuut from config file.
        """
        try:
            for i in range(self.preuut_start + 1, self.preuut_end):
                if '##' in self.sequence_file[i]:
                    continue
                if ',,,' in self.sequence_file[i]:
                    continue
                match self.sequence_file[i].split(',')[1]:
                    case 'serial':
                        match self.sequence_file[i].split(',')[3]:
                            case 'open':
                                Rs232.open(Rs232(globals()['serialCom' + self.sequence_file[i].split(',')[2]],
                                                 int(globals()['serialBaud' + self.sequence_file[i].split(',')[2]]),
                                                 int(globals()['serialBytesize' + self.sequence_file[i].split(',')[2]]),
                                                 globals()['serialParity' + self.sequence_file[i].split(',')[2]],
                                                 int(globals()['serialStopbits' + self.sequence_file[i].split(',')[2]]),
                                                 int(globals()['serialTimeout' + self.sequence_file[i].split(',')[2]])), self.thread_number)
                            case _:
                                pass
                    case 'wait':
                        sleep(int(self.sequence_file[i].split(',')[3]))
                    case _:
                        pass
        except (Exception, BaseException):
            print('Error 0x200 Undefined error in sequence call. ' + format_exc())
            Logger.log_event(Logger(), 'Error 0x200 Undefined error in sequence call. ' + format_exc())

    def sequence_read(self):
        """
        Process the sequence file.
        """
        try:
            for i in range(self.sequence_start + 1, self.sequence_end):
                if '##' in self.sequence_file[i]:
                    continue
                if ',,,' in self.sequence_file[i]:
                    continue
                match self.sequence_file[i].split(',')[1]:
                    case 'serial':
                        match self.sequence_file[i].split(',')[3]:
                            case 'write':
                                Rs232.write(self, str(self.sequence_file[i].split(',')[4]), self.sequence_file[i].split(',')[2])
                            case 'read':
                                globals()[str(self.sequence_file[i].split(',')[4])] = (
                                    Rs232.read(self, str(self.sequence_file[i].split(',')[2])))
                                if str(self.sequence_file[i].split(',')[4]) == 'serial_number':
                                    lib.shared_variables.serial_number = globals()[str('serial_number')]
                            case _:
                                pass
                    case 'wait':
                        sleep(int(self.sequence_file[i].split(',')[3]))
                    case _:
                        pass
        except (Exception, BaseException):
            print('Error 0x200 Undefined error in sequence call. ' + format_exc())
            Logger.log_event(Logger(), 'Error 0x200 Undefined error in sequence call. ' + format_exc())

    def postuut_read(self):
        """
        Read postuut from config file.
        """
        try:
            for i in range(self.postuut_start + 1, self.postuut_end):
                if '##' in self.sequence_file[i]:
                    continue
                if ',,,' in self.sequence_file[i]:
                    continue
                match self.sequence_file[i].split(',')[1]:
                    case 'serial':
                        match self.sequence_file[i].split(',')[3]:
                            case 'close':
                                Rs232.close(self.sequence_file[i].split(',')[2])
                            case _:
                                pass
                    case _:
                        pass
        except (Exception, BaseException):
            print('Error 0x200 Undefined error in sequence call. ' + format_exc())
            Logger.log_event(Logger(), 'Error 0x300 Undefined error in sequence call. ' + format_exc())

