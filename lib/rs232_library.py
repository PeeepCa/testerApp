# RS232 communication library

from serial import Serial, serialutil
from ctypes import windll
from traceback import format_exc

from lib.logger_library import Logger

msg_show = 1
ser = Serial()


class Rs232:
    """
    Hardware handling for RS232.
    :param com: COM of instrument
    :param baud: BAUD of instrument
    :param timeout: timeout for communication
    """
    def __init__(self, com, baud, timeout):
        # input of COM and BAUD
        self.COM = com
        self.BAUD = baud
        self.timeout = timeout

    def open(self):
        """
        Open the RS232
        """
        try:
            globals()['ser'] = Serial(self.COM, self.BAUD, timeout=self.timeout)
        except serialutil.SerialException:
            if msg_show == 1:
                windll.user32.MessageBoxW(0, 'Error 0x203 RS232 at: ' + self.COM + ' cannot be found.',
                                          'HW Error', 0x1000)
                Logger.log_event(Logger(), 'RS232 reader at ' + self.COM +
                                 ' doesnt work' + format_exc())

    def write(self, command):
        """
        RS232 write
        :param command: command which zou want to send
        :return: serial_string
        """
        try:
            ser.write(command.encode('utf-8'))

        except serialutil.SerialException:
            Logger.log_event(Logger(), 'RS232 reader trying to reconnect. ' + format_exc())
            Rs232.close()
            global msg_show
            msg_show = 0
            Rs232.open(Rs232(self.COM, self.BAUD, self.timeout))
            msg_show = 1

    def read(self):
        """
        RS232 read
        :return: serial_string
        """
        try:
            # TODO: switch after implementation
            serial_string = ser.readline()
            # serial_string = ser.read_until(b'\r\n', 8)
            return serial_string
        except serialutil.SerialException:
            Logger.log_event(Logger(), 'RS232 reader trying to reconnect. ' + format_exc())
            Rs232.close()
            global msg_show
            msg_show = 0
            Rs232.open(Rs232(self.COM, self.BAUD, self.timeout))
            msg_show = 1

    @staticmethod
    def close():
        """
        Close the RS232
        """
        ser.close()
