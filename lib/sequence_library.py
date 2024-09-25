import lib.shared_varriables

from lib.logger_library import Logger
from ctypes import windll
from traceback import format_exc
from lib.rs232_library import Rs232
from tkinter import simpledialog


class Sequence:
    """
    Calling the sequence file to process it.
    :param file: path to the sequence file
    """
    def __init__(self, file):
        file = open(file, 'r')
        self.sequence_file = file.read(-1).splitlines()
        file.close()

    def sequence_read(self):
        """
        Process the sequence file.
        """
        try:
            for sequence_step in self.sequence_file:
                match sequence_step.split('.')[0]:
                    case '' | ' ' | None | '#':
                        continue
                    case 'READ_SN':
                        if lib.shared_varriables.useReader:
                            Rs232.write(self, 'LON,01\r')
                            lib.shared_varriables.serial_number = str(Rs232.read(self))
                            Rs232.write(self, 'LOFF\r')
                        else:
                            lib.shared_varriables.serial_number = simpledialog.askstring("New Item", "Enter name of item:")

        except (Exception, BaseException):
            windll.user32.MessageBoxW(0, 'Error 0x100 Undefined error in sequence call.' + format_exc(), 'Error', 0x1000)
            Logger.log_event(Logger(), 'Error 0x100 Undefined error in sequence call. ' + format_exc())

