# RS232 communication library

from serial import Serial, serialutil
from ctypes import windll
from traceback import format_exc

from lib.logger_library import Logger


class Rs232:
    """
    Hardware handling for RS232.v
    :param com: COM of instrument
    :param baud: BAUD of instrument
    :param bytesize: bytesize for communication
    :param parity: parity for communication
    :param stopbits: stopbits for communication
    :param timeout: timeout for communication
    """
    def __init__(self, com, baud, bytesize, parity, stopbits, timeout):
        # input of COM and BAUD
        self.COM = com
        self.BAUD = baud
        self.bytesize = bytesize
        self.parity = parity
        self.stopbits = stopbits
        self.timeout = timeout
        globals()['msg_show'] = 1

    def open(self, com_number):
        """
        Open the RS232
        :param com_number: COM number
        """
        try:
            globals()['ser' + str(com_number)] = Serial(self.COM, baudrate=self.BAUD, bytesize=self.bytesize, parity=self.parity, stopbits=self.stopbits, timeout=self.timeout)
            status = 0
        except serialutil.SerialException:
            if globals()['msg_show'] == 1:
                windll.user32.MessageBoxW(0, 'Error 0x200 RS232 reader at: ' + self.COM + ' cannot be found.',
                                          'HW Error', 0x1000)
                Logger.log_event(Logger(), 'Error 0x200 RS232 reader at ' + self.COM +
                                 ' cannot be found' + format_exc())
            status = 1
        return  status

    def write(self, command, com_number):
        """
        RS232 write
        :param command: command which zou want to send
        :param com_number: COM number
        :return: serial_string
        """
        try:
            command = command.encode('utf-8').replace(b'\\r', b'\r')
            globals()['ser' + str(com_number)].write(command)
            status = 0
        except serialutil.SerialException:
            Logger.log_event(Logger(), 'RS232 reader trying to reconnect. ' + format_exc())
            Rs232.close(com_number)
            globals()['msg_show'] = 0
            Rs232.open(Rs232(self.COM, self.BAUD, self.timeout, self.bytesize, self.parity, self.stopbits), com_number)
            globals()['msg_show'] = 1
            status = 1
        return status

    def read(self, com_number):
        """
        RS232 read
        :param com_number: COM number
        :return: serial_string
        """
        try:
            # TODO: switch after implementation
            serial_string = globals()['ser' + str(com_number)].readline()
            # serial_string = globals()['ser' + str(com_number)].read_until(b'\r\n', 8)
            status = 0
        except serialutil.SerialException:
            Logger.log_event(Logger(), 'RS232 reader trying to reconnect. ' + format_exc())
            Rs232.close(com_number)
            globals()['msg_show'] = 0
            Rs232.open(Rs232(self.COM, self.BAUD, self.timeout, self.bytesize, self.parity, self.stopbits), com_number)
            globals()['msg_show'] = 1
            status = 1
            serial_string = b''
        return status, serial_string.decode('utf-8')

    @staticmethod
    def close(com_number):
        """
        Close the RS232
        :param com_number: COM number
        """
        globals()['ser' + str(com_number)].close()
