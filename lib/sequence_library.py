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

    def parse_sequence_file(self):
        """
        Parse the sequence file.
        :return:
        """
        settings_start = None
        settings_end = None
        preuut_start = None
        preuut_end = None
        sequence_start = None
        sequence_end = None
        postuut_start = None
        postuut_end = None

        size = len(self.sequence_file)

        for settings_size in range(size):
            if '[SETTINGS]' in self.sequence_file[settings_size]:
                settings_start = settings_size
            elif '[SETTINGS_END]' in self.sequence_file[settings_size]:
                settings_end = settings_size
                break

        for preuut_size in range(size):
            if '[PREUUT]' in self.sequence_file[preuut_size]:
                preuut_start = preuut_size
            elif '[PREUUT_END]' in self.sequence_file[preuut_size]:
                preuut_end = preuut_size
                break

        for sequence_size in range(size):
            if '[SEQUENCE]' in self.sequence_file[sequence_size]:
                sequence_start = sequence_size
            elif '[SEQUENCE_END]' in self.sequence_file[sequence_size]:
                sequence_end = sequence_size
                break

        for postuut_size in range(size):
            if '[POSTUUT]' in self.sequence_file[postuut_size]:
                postuut_start = postuut_size
            elif '[POSTUUT_END]' in self.sequence_file[postuut_size]:
                postuut_end = postuut_size
                break

        return (settings_start, settings_end, preuut_start, preuut_end, sequence_start,
                sequence_end, postuut_start, postuut_end)

    def settings_read(self, settings_start, settings_end):
        """
        Read the settings from the sequence file.
        :param settings_start: Line for start of settings
        :param settings_end: Line for end of settings
        :return:
        """
        try:
            for i in range(settings_start + 1, settings_end):
                if '##' in self.sequence_file[i]:
                    continue
                if ',,,' in self.sequence_file[i]:
                    continue
                match self.sequence_file[i].split(',')[1]:
                    case 'stationNumber':
                        self.station_number = self.sequence_file[i].split(',')[4]
                    case 'processLayer':
                        self.process_layer = self.sequence_file[i].split(',')[4]
                    case 'restApi':
                        self.restApi = self.sequence_file[i].split(',')[4]
                    case 'serialCom':
                        globals()[str(self.sequence_file[i].split(',')[1] +
                                      self.sequence_file[i].split(',')[2])] = self.sequence_file[i].split(',')[4]
                    case 'serialBaud':
                        globals()[str(self.sequence_file[i].split(',')[1] +
                                      self.sequence_file[i].split(',')[2])] = self.sequence_file[i].split(',')[4]
                    case 'serialBytesize':
                        globals()[str(self.sequence_file[i].split(',')[1] +
                                      self.sequence_file[i].split(',')[2])] = self.sequence_file[i].split(',')[4]
                    case 'serialParity':
                        globals()[str(self.sequence_file[i].split(',')[1] +
                                      self.sequence_file[i].split(',')[2])] = self.sequence_file[i].split(',')[4]
                    case 'serialStopbits':
                        globals()[str(self.sequence_file[i].split(',')[1] +
                                      self.sequence_file[i].split(',')[2])] = self.sequence_file[i].split(',')[4]
                    case 'serialTimeout':
                        globals()[str(self.sequence_file[i].split(',')[1] +
                                      self.sequence_file[i].split(',')[2])] = self.sequence_file[i].split(',')[4]
                    case _:
                        pass
        except (Exception, BaseException):
            print('Error 0x101 Undefined error in sequence call. ' + format_exc())
            Logger.log_event(Logger(), 'Error 0x101 Undefined error in sequence call. ' + format_exc())

    def sequence_read(self, sequence_start, sequence_end):
        """
        Read the sequence from the sequence file.
        :param sequence_start: Line for start of sequence
        :param sequence_end: Line for end of sequence
        :return:
        """
        try:
            for i in range(sequence_start + 1, sequence_end):
                print(self.sequence_file[i])
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
                                                 int(globals()['serialTimeout' + self.sequence_file[i].split(',')[2]])),
                                           self.thread_number)
                            case 'write':
                                Rs232.write(self, str(self.sequence_file[i].split(',')[4]), self.sequence_file[i].split(',')[2])
                            case 'read':
                                globals()[str(self.sequence_file[i].split(',')[5])] = (
                                    Rs232.read(self, str(self.sequence_file[i].split(',')[2])))
                                if str(self.sequence_file[i].split(',')[5]) == 'serial_number':
                                    lib.shared_variables.serial_number = globals()[str('serial_number')]
                            case 'close':
                                Rs232.close(self.sequence_file[i].split(',')[2])
                            case _:
                                pass
                    case 'wait':
                        sleep(int(self.sequence_file[i].split(',')[3]))
                    case _:
                        pass
        except (Exception, BaseException):
            print('Error 0x100 Undefined error in sequence call. ' + format_exc())
            Logger.log_event(Logger(), 'Error 0x200 Undefined error in sequence call. ' + format_exc())

        except (Exception, BaseException):
            print('Error 0x100 Undefined error in sequence call. ' + format_exc())
            Logger.log_event(Logger(), 'Error 0x300 Undefined error in sequence call. ' + format_exc())

