import lib.shared_variables

from traceback import format_exc
from time import sleep

from lib.logger_library import Logger
from lib.rs232_library import Rs232
from lib.itac_library import Itac


class Sequence:
    """
    Calling the sequence file to process it.
    """
    def __init__(self):
        self.settings_start = None
        self.settings_end = None
        self.preuut_start = None
        self.preuut_end = None
        self.sequence_start = None
        self.sequence_end = None
        self.postuut_start = None
        self.postuut_end = None
        self.sequence_file = None

    def parse_sequence_file(self,file):
        """
        Parse the sequence file.
        :param file: File to parse
        :return:
        """

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
            if '[POSTUUT]' in self.sequence_file[postuut_size]:
                self.postuut_start = postuut_size
            elif '[POSTUUT_END]' in self.sequence_file[postuut_size]:
                self.postuut_end = postuut_size
                break

        return (self.sequence_file, self.settings_start, self.settings_end, self.preuut_start, self.preuut_end, self.sequence_start,
                self.sequence_end, self.postuut_start, self.postuut_end)

    def settings_read(self, sequence_file, settings_start, settings_end, thread_number):
        """
        Read the settings from the sequence file.
        :param sequence_file: File to read
        :param settings_start: Line for start of settings
        :param settings_end: Line for end of settings
        :param thread_number: Thread number
        :return:
        """
        try:
            self.sequence_file = sequence_file
            for i in range(settings_start + 1, settings_end):
                print(self.sequence_file[i])
                if '##' in self.sequence_file[i]:
                    continue
                if ';;;;' in self.sequence_file[i]:
                    continue
                if int(self.sequence_file[i].split(';')[0]) == int(thread_number):
                    match self.sequence_file[i].split(';')[1]:
                        case 'stationNumber':
                            globals()[str('station_number')] = self.sequence_file[i].split(';')[4]
                        case 'processLayer':
                            globals()[str('process_layer')] = self.sequence_file[i].split(';')[4]
                        case 'restApi':
                            globals()[str('restApi')] = self.sequence_file[i].split(';')[4]
                        case 'serialCom':
                            globals()[str(self.sequence_file[i].split(';')[1] +
                                          self.sequence_file[i].split(';')[2])] = self.sequence_file[i].split(';')[4]
                        case 'serialBaud':
                            globals()[str(self.sequence_file[i].split(';')[1] +
                                          self.sequence_file[i].split(';')[2])] = self.sequence_file[i].split(';')[4]
                        case 'serialBytesize':
                            globals()[str(self.sequence_file[i].split(';')[1] +
                                          self.sequence_file[i].split(';')[2])] = self.sequence_file[i].split(';')[4]
                        case 'serialParity':
                            globals()[str(self.sequence_file[i].split(';')[1] +
                                          self.sequence_file[i].split(';')[2])] = self.sequence_file[i].split(';')[4]
                        case 'serialStopbits':
                            globals()[str(self.sequence_file[i].split(';')[1] +
                                          self.sequence_file[i].split(';')[2])] = self.sequence_file[i].split(';')[4]
                        case 'serialTimeout':
                            globals()[str(self.sequence_file[i].split(';')[1] +
                                          self.sequence_file[i].split(';')[2])] = self.sequence_file[i].split(';')[4]
                        case _:
                            pass
                else:
                    continue
        except (Exception, BaseException):
            print('Error 0x101 Undefined error in sequence call. ' + format_exc())
            Logger.log_event(Logger(), 'Error 0x101 Undefined error in sequence call. ' + format_exc())

    def sequence_read(self, sequence_file, sequence_start, sequence_end, thread_number):
        """
        Read the sequence from the sequence file.
        :param sequence_file: File to read
        :param sequence_start: Line for start of sequence
        :param sequence_end: Line for end of sequence
        :param thread_number: Thread number
        :return:
        """
        try:
            self.sequence_file = sequence_file
            for i in range(sequence_start + 1, sequence_end):
                print(self.sequence_file[i])
                if '##' in self.sequence_file[i]:
                    continue
                if ';;;;' in self.sequence_file[i]:
                    continue
                if int(self.sequence_file[i].split(';')[0]) == int(thread_number):
                    match self.sequence_file[i].split(';')[1]:
                        case 'serial':
                            match self.sequence_file[i].split(';')[3]:
                                case 'open':
                                    Rs232.open(Rs232(globals()['serialCom' + self.sequence_file[i].split(';')[2]],
                                                     int(globals()['serialBaud' + self.sequence_file[i].split(';')[2]]),
                                                     int(globals()['serialBytesize' + self.sequence_file[i].split(';')[2]]),
                                                     globals()['serialParity' + self.sequence_file[i].split(';')[2]],
                                                     int(globals()['serialStopbits' + self.sequence_file[i].split(';')[2]]),
                                                     int(globals()['serialTimeout' + self.sequence_file[i].split(';')[2]])),
                                               self.sequence_file[i].split(';')[2])
                                case 'write':
                                    Rs232.write(self, str(self.sequence_file[i].split(';')[4]), self.sequence_file[i].split(';')[2])
                                case 'read':
                                    globals()[str(self.sequence_file[i].split(';')[5])] = (
                                        Rs232.read(self, str(self.sequence_file[i].split(';')[2])))
                                    if str(self.sequence_file[i].split(';')[5]) == 'serial_number':
                                        lib.shared_variables.serial_number = globals()[str('serial_number')]
                                case 'close':
                                    Rs232.close(self.sequence_file[i].split(';')[2])
                                case _:
                                    pass
                        case 'itac':
                            match self.sequence_file[i].split(';')[3]:
                                case 'login':
                                    Itac.login(Itac(globals()['station_number'], globals()['restApi']))
                                case 'logout':
                                    Itac.logout(Itac(globals()['station_number'], globals()['restApi']))
                        case 'wait':
                            sleep(int(self.sequence_file[i].split(';')[4]))
                        case _:
                            pass
                else:
                    continue
        except (Exception, BaseException):
            print('Error 0x100 Undefined error in sequence call. ' + format_exc())
            Logger.log_event(Logger(), 'Error 0x200 Undefined error in sequence call. ' + format_exc())
