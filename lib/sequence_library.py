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
        self.logger = Logger()

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
        lib.shared_variables.step_name = sequence_file[line_index]
        print(sequence_file[line_index])
        line = sequence_file[line_index]
        if line.split(';')[0] == str(thread_number):
            match line.split(';')[1]:
                case 'serial':
                    self.handle_serial_command(line)
                case 'itac':
                    self.handle_itac_command(line)
                case 'wait':
                    self.handle_wait_command(line)
                case 'stationNumber':
                    self.handle_settings_static(line)
                case 'processLayer':
                    self.handle_settings_static(line)
                case 'restApi':
                    self.handle_settings_static(line)
                case 'serialCom':
                    self.handle_settings_dynamic(line)
                case 'serialBaud':
                    self.handle_settings_dynamic(line)
                case 'serialBytesize':
                    self.handle_settings_dynamic(line)
                case 'serialParity':
                    self.handle_settings_dynamic(line)
                case 'serialStopbits':
                    self.handle_settings_dynamic(line)
                case 'serialTimeout':
                    self.handle_settings_dynamic(line)

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
            self.logger.log_event('Error 0x201 Step not found. ' + format_exc())
        except (Exception, BaseException):
            print('Error 0x201 Undefined error in serial command. ' + format_exc())
            self.logger.log_event('Error 0x201 Undefined error in serial command. ' + format_exc())

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
            print('Error 0x202 Undefined error in itac command. ' + format_exc())
            self.logger.log_event('Error 0x202 Undefined error in itac command. ' + format_exc())

    def handle_wait_command(self, line):
        """
        Handle the wait command.
        :param line: Line read
        :return:
        """
        try:
            self.wait(line)
        except (Exception, BaseException):
            print('Error 0x203 Undefined error in wait command. ' + format_exc())
            self.logger.log_event('Error 0x203 Undefined error in wait command. ' + format_exc())

    def handle_settings_dynamic(self, line):
        """
        Handle the settings command.
        :param line: Line read
        :return:
        """
        try:
            self.settings_dynamic(line)
        except (Exception, BaseException):
            print('Error 0x204 Undefined error in settings command. ' + format_exc())
            self.logger.log_event('Error 0x204 Undefined error in settings command. ' + format_exc())

    def handle_settings_static(self, line):
        """
        Handle the settings command.
        :param line: Line read
        :return:
        """
        try:
            self.settings_static(line)
        except (Exception, BaseException):
            print('Error 0x204 Undefined error in settings command. ' + format_exc())
            self.logger.log_event('Error 0x204 Undefined error in settings command. ' + format_exc())

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
        Itac.login(Itac(globals()['stationNumber'], globals()['restApi']))

    @staticmethod
    def logout_itac():
        """
        Logout from iTAC.
        :return:
        """
        Itac.logout(Itac(globals()['stationNumber'], globals()['restApi']))

    @staticmethod
    def wait(line):
        """
        Wait for given time in milliseconds.
        :param line: Line read
        :return:
        """
        sleep(int(line.split(';')[4]))

    @staticmethod
    def settings_dynamic(line):
        """
        Set settings.
        :param line: Line read
        :return:
        """
        globals()[str(line.split(';')[1] + line.split(';')[2])] = line.split(';')[4]

    @staticmethod
    def settings_static(line):
        """
        Set settings.
        :param line: Line read
        :return:
        """
        globals()[str(line.split(';')[1])] = line.split(';')[4]