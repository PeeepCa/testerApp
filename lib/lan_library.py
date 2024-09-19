# LAN communication library

import socket


class Lan:
    """
    Hardware handling for LAN
    :param ip: IP address for instrument
    :param port: Port for instrument
    :param timeout: Timeout for communication
    """
    def __init__(self, ip, port, timeout):
        self.ip = ip
        self.port = port
        self.timeout = timeout

    def open(self):
        """
        Opens the communication via LAN
        """
        globals()['s'] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        globals()['s'].settimeout(self.timeout)
        globals()['s'].connect((self.ip, self.port))

    @staticmethod
    def send(command):
        """
        Send command via LAN
        :param command: Command which you want to send
        :return:
        """
        globals()['s'].send(command)

    @staticmethod
    def receive():
        """
        Receive message via LAN
        :return:
        """
        message = globals()['s'].revc(128)
        return message

    @staticmethod
    def close():
        """
        Close the communication
        :return:
        """
        globals()['s'].close()
