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
        pass

    # @staticmethod
    # def parse_sequence_file(file):
    #     """
    #     Parse the sequence file.
    #     :param file: File to parse
    #     :return:
    #     """
    #     settings_start = 0
    #     settings_end = 0
    #     preuut_start = 0
    #     preuut_end = 0
    #     sequence_start = 0
    #     sequence_end = 0
    #     postuut_start = 0
    #     postuut_end = 0
    #
    #     file = open(file, 'r')
    #     sequence_file = file.read(-1).splitlines()
    #     file.close()
    #
    #     size = len(sequence_file)
    #
    #     for settings_size in range(size):
    #         if '[SETTINGS]' in sequence_file[settings_size]:
    #             settings_start = settings_size
    #         elif '[SETTINGS_END]' in sequence_file[settings_size]:
    #             settings_end = settings_size
    #             break
    #
    #     for preuut_size in range(size):
    #         if '[PREUUT]' in sequence_file[preuut_size]:
    #             preuut_start = preuut_size
    #         elif '[PREUUT_END]' in sequence_file[preuut_size]:
    #             preuut_end = preuut_size
    #             break
    #
    #     for sequence_size in range(size):
    #         if '[SEQUENCE]' in sequence_file[sequence_size]:
    #             sequence_start = sequence_size
    #         elif '[SEQUENCE_END]' in sequence_file[sequence_size]:
    #             sequence_end = sequence_size
    #             break
    #
    #     for postuut_size in range(size):
    #         if '[POSTUUT]' in sequence_file[postuut_size]:
    #             postuut_start = postuut_size
    #         elif '[POSTUUT_END]' in sequence_file[postuut_size]:
    #             postuut_end = postuut_size
    #             break
    #
    #     return (sequence_file, settings_start, settings_end, preuut_start, preuut_end, sequence_start,
    #             sequence_end, postuut_start, postuut_end)

    @staticmethod
    def read_sequence_file(file):
        """
        Read the sequence file.
        :param file: File to read
        :return:
        """
        file = open(file, 'r')
        sequence_file = file.read(-1).splitlines()
        file.close()
        return sequence_file

    def parse_sequence_file(self, file):
        """
        Parse the sequence file.
        :param file: File to parse
        :return:
        """
        sequence_file = self.read_sequence_file(file)
        sections = {
            '[SETTINGS]': ('[SETTINGS_END]', 'settings'),
            '[PREUUT]': ('[PREUUT_END]', 'preuut'),
            '[SEQUENCE]': ('[SEQUENCE_END]', 'sequence'),
            '[POSTUUT]': ('[POSTUUT_END]', 'postuut')
        }
        section_indices = {}
        for section_start, (section_end, section_name) in sections.items():
            start_index = None
            end_index = None
            for i, line in enumerate(sequence_file):
                if section_start in line:
                    start_index = i
                elif section_end in line:
                    end_index = i
                    break
            section_indices[section_name] = (start_index, end_index)
        return sequence_file, *section_indices.values()

    @staticmethod
    def settings_read(sequence_file, settings_start, settings_end, thread_number):
        """
        Read the settings from the sequence file.
        :param sequence_file: File to read
        :param settings_start: Line for start of settings
        :param settings_end: Line for end of settings
        :param thread_number: Thread number
        :return:
        """
        try:
            for i in range(settings_start + 1, settings_end):
                if '##' in sequence_file[i]:
                    continue
                elif ';;;;' in sequence_file[i]:
                    continue
                elif int(sequence_file[i].split(';')[0]) == int(thread_number):
                    match sequence_file[i].split(';')[1]:
                        case 'stationNumber':
                            globals()[str('station_number')] = sequence_file[i].split(';')[4]
                        case 'processLayer':
                            globals()[str('process_layer')] = sequence_file[i].split(';')[4]
                        case 'restApi':
                            globals()[str('restApi')] = sequence_file[i].split(';')[4]
                        case 'serialCom':
                            globals()[str(sequence_file[i].split(';')[1] +
                                          sequence_file[i].split(';')[2])] = sequence_file[i].split(';')[4]
                        case 'serialBaud':
                            globals()[str(sequence_file[i].split(';')[1] +
                                          sequence_file[i].split(';')[2])] = sequence_file[i].split(';')[4]
                        case 'serialBytesize':
                            globals()[str(sequence_file[i].split(';')[1] +
                                          sequence_file[i].split(';')[2])] = sequence_file[i].split(';')[4]
                        case 'serialParity':
                            globals()[str(sequence_file[i].split(';')[1] +
                                          sequence_file[i].split(';')[2])] = sequence_file[i].split(';')[4]
                        case 'serialStopbits':
                            globals()[str(sequence_file[i].split(';')[1] +
                                          sequence_file[i].split(';')[2])] = sequence_file[i].split(';')[4]
                        case 'serialTimeout':
                            globals()[str(sequence_file[i].split(';')[1] +
                                          sequence_file[i].split(';')[2])] = sequence_file[i].split(';')[4]
                        case _:
                            pass
                else:
                    continue
        except (Exception, BaseException):
            print('Error 0x101 Undefined error in sequence call. ' + format_exc())
            Logger.log_event(Logger(), 'Error 0x104 Undefined error in sequence call. ' + format_exc())

    # def sequence_read(self, sequence_file, sequence_start, sequence_end, thread_number):
    #     """
    #     Read the sequence from the sequence file.
    #     :param sequence_file: File to read
    #     :param sequence_start: Line for start of sequence
    #     :param sequence_end: Line for end of sequence
    #     :param thread_number: Thread number
    #     :return:
    #     """
    #     try:
    #         for i in range(sequence_start + 1, sequence_end):
    #             try:
    #                 previous_status = lib.shared_variables.status
    #                 if '##' in sequence_file[i]:
    #                     continue
    #                 if ';;;;' in sequence_file[i]:
    #                     continue
    #                 if int(sequence_file[i].split(';')[0]) == int(thread_number):
    #                     match sequence_file[i].split(';')[1]:
    #                         case 'serial':
    #                             match sequence_file[i].split(';')[3]:
    #                                 case 'open':
    #                                     lib.shared_variables.status += Rs232.open(Rs232(globals()['serialCom' + sequence_file[i].split(';')[2]],
    #                                                      int(globals()['serialBaud' + sequence_file[i].split(';')[2]]),
    #                                                      int(globals()['serialBytesize' + sequence_file[i].split(';')[2]]),
    #                                                      globals()['serialParity' + sequence_file[i].split(';')[2]],
    #                                                      int(globals()['serialStopbits' + sequence_file[i].split(';')[2]]),
    #                                                      int(globals()['serialTimeout' + sequence_file[i].split(';')[2]])),
    #                                                sequence_file[i].split(';')[2])
    #                                 case 'write':
    #                                     lib.shared_variables.status += Rs232.write(self, str(sequence_file[i].split(';')[4]), sequence_file[i].split(';')[2])
    #                                 case 'read':
    #                                     status, globals()[str(sequence_file[i].split(';')[5])] = (
    #                                         Rs232.read(self, str(sequence_file[i].split(';')[2])))
    #                                     lib.shared_variables.status += status
    #                                     if str(sequence_file[i].split(';')[5]) == 'serial_number':
    #                                         lib.shared_variables.serial_number = globals()[str('serial_number')]
    #                                 case 'close':
    #                                     Rs232.close(sequence_file[i].split(';')[2])
    #                                 case _:
    #                                     pass
    #                         case 'itac':
    #                             match sequence_file[i].split(';')[3]:
    #                                 case 'login':
    #                                     Itac.login(Itac(globals()['station_number'], globals()['restApi']))
    #                                 case 'logout':
    #                                     Itac.logout(Itac(globals()['station_number'], globals()['restApi']))
    #                         case 'wait':
    #                             sleep(int(sequence_file[i].split(';')[4]))
    #                         case _:
    #                             pass
    #                 else:
    #                     continue
    #                 if lib.shared_variables.status != previous_status:
    #                     # noinspection PyUnusedLocal
    #                     previous_status = lib.shared_variables.status
    #             except KeyError:
    #                 Logger.log_event(Logger(), 'Error 0x102 KeyError, global variable not found. ' + format_exc())
    #                 continue
    #     except (Exception, BaseException):
    #         print('Error 0x100 Undefined error in sequence call. ' + format_exc())
    #         Logger.log_event(Logger(), 'Error 0x100 Undefined error in sequence call. ' + format_exc())

    def sequence_read(self, sequence_file, sequence_start, sequence_end, thread_number):
        """
        Read the sequence from the sequence file.
        :param sequence_file: File to read
        :param sequence_start: Line for start of sequence
        :param sequence_end: Line for end of sequence
        :param thread_number: Thread number
        :return:
        """
        for i in range(sequence_start + 1, sequence_end):
            self.process_sequence_line(sequence_file, i, thread_number)

    def process_sequence_line(self, sequence_file, line_index, thread_number):
        """
        Process the line in the sequence file.
        :param sequence_file: File to read
        :param line_index: Line to process
        :param thread_number: Thread number
        :return:
        """
        line = sequence_file[line_index]
        if line.split(';')[0] == str(thread_number):
            match line.split(';')[1]:
                case 'serial':
                    self.handle_serial_command(line)
                case 'itac':
                    self.handle_itac_command(line)
                case 'wait':
                    self.handle_wait_command(line)
                case _:
                    pass

    def handle_serial_command(self, line):
        """
        Handle the serial command.
        :param line: Line read
        :return:
        """
        try:
            match line.split(';')[3]:
                case 'open':
                    self.open_serial(line)
                case 'write':
                    self.write_serial(line)
                case 'read':
                    self.read_serial(line)
                case 'close':
                    self.close_serial(line)
        except KeyError:
            Logger.log_event(Logger(), 'Error 0x101 Undefined error in serial command. ' + format_exc())
        except (Exception, BaseException):
            print('Error 0x101 Undefined error in serial command. ' + format_exc())
            Logger.log_event(Logger(), 'Error 0x101 Undefined error in serial command. ' + format_exc())

    def handle_itac_command(self, line):
        """
        Handle the itac command.
        :param line: Line read
        :return:
        """
        try:
            match line.split(';')[3]:
                case 'login':
                    self.login_itac()
                case 'logout':
                    self.logout_itac()
        except (Exception, BaseException):
            print('Error 0x102 Undefined error in itac command. ' + format_exc())
            Logger.log_event(Logger(), 'Error 0x102 Undefined error in itac command. ' + format_exc())

    def handle_wait_command(self, line):
        """
        Handle the wait command.
        :param line: Line read
        :return:
        """
        try:
            self.wait(line)
        except (Exception, BaseException):
            print('Error 0x103 Undefined error in wait command. ' + format_exc())
            Logger.log_event(Logger(), 'Error 0x103 Undefined error in wait command. ' + format_exc())

    @staticmethod
    def open_serial(line):
        lib.shared_variables.status += Rs232.open(Rs232(globals()['serialCom' + line.split(';')[2]],
                                                             int(globals()['serialBaud' + line.split(';')[2]]),
                                                             int(globals()['serialBytesize' + line.split(';')[2]]),
                                                             globals()['serialParity' + line.split(';')[2]],
                                                             int(globals()['serialStopbits' + line.split(';')[2]]),
                                                             int(globals()['serialTimeout' + line.split(';')[2]])),
                                                       line.split(';')[2])

    def write_serial(self, line):
        """
        Write to the serial port.
        :param line: Line read
        :return:
        """
        lib.shared_variables.status += Rs232.write(self, str(line.split(';')[4]),
                                                   line.split(';')[2])

    def read_serial(self, line):
        """
        Read from the serial port.
        :param line: Line read
        :return:
        """
        status, globals()[str(line.split(';')[5])] = (Rs232.read(self, str(line.split(';')[2])))
        lib.shared_variables.status += status
        if str(line.split(';')[5]) == 'serial_number':
            lib.shared_variables.serial_number = globals()[str('serial_number')]

    @staticmethod
    def close_serial(line):
        """
        Close the serial port.
        :param line: Line read
        :return:
        """
        Rs232.close(line.split(';')[2])

    @staticmethod
    def login_itac():
        """
        Login to iTAC.
        :return:
        """
        Itac.login(Itac(globals()['station_number'], globals()['restApi']))

    @staticmethod
    def logout_itac():
        """
        Logout from iTAC.
        :return:
        """
        Itac.logout(Itac(globals()['station_number'], globals()['restApi']))

    @staticmethod
    def wait(line):
        """
        Wait for given time in milliseconds.
        :param line: Line read
        :return:
        """
        sleep(int(line.split(';')[4]))
