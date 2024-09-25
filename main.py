# TesterAPP

# Error list:
# 0x000 Undefined error in main.
# 0x100 Undefined error in sequence call.

# TODO:
#  Multithreading for parallel testing
#  GUI with dynamic UI for testing
#  ** Config file stored on server - Done
#  Auto updating like PEPO
#  ** Logging to server log file - reused from PEPO
#  Error handling inside the APP
#  iTAC via restAPI
#  SESO via restAPI
#  ** HW library - rs232 done with timeout which need to be defined
#  Muster
#  ** Sequence implementation for testing - Partially done
#  Selftest for relay cards
#  Relay control from tab in app
#  Reader AUTO/MANUAL to global variable

import sys
import lib.shared_variables as shared_variables

from socket import gethostname
from os import path
from traceback import format_exc
from ctypes import windll

from lib.sequence_library import Sequence
from lib.logger_library import Logger
from lib.config_library import Config
from lib.rs232_library import Rs232
from lib.itac_library import Itac


class Main:
    def __init__(self):
        Logger.log_event(Logger(), 'Logging started.')
        if getattr(sys, 'frozen', False):
            self.application_path = path.dirname(sys.executable)
        elif __file__:
            self.application_path = path.dirname(__file__)
        else:
            self.application_path = None
        try:
            temp = Config.read_config(Config(self.application_path + '/config/'
                                             + gethostname() + '.ini'))
        except FileNotFoundError:
            windll.user32.MessageBoxW(0, 'Error 0x100 Config file not found', 'Error', 0x1000)
            Logger.log_event(Logger(), 'Error 0x100 Config file not found. ' + format_exc())
            sys.exit()
        self.stationNumber = temp[0]
        self.restAPI = temp[1]
        self.useITAC = temp[2]
        self.processLayer = temp[3]
        self.useReader = temp[4]
        self.readerCom = temp[5]
        self.readerBaud = temp[6]
        self.readerBytesize = temp[7]
        self.readerParity = temp[8]
        self.readerStopbits = temp[9]
        self.readerTimeout = temp[10]
        shared_variables.useReader = self.useReader
        shared_variables.useITAC = self.useITAC

        if self.useReader:
            Rs232.open(Rs232(self.readerCom, self.readerBaud, self.readerBytesize, self.readerParity, self.readerStopbits, self.readerTimeout))
        if self.useITAC:
            Itac.login(Itac(self.stationNumber, self.restAPI))

    @staticmethod
    def test(__):
        # test procedure
        Sequence.sequence_read(Sequence('main.program'))
        print(shared_variables.serial_number)

Main.test(Main())