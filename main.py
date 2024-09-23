# TesterAPP

# Error list:
# 0x000 Undefined error in main.
# 0x100 Undefined error in sequence call.

# TODO:
#  Multithreading for parallel testing
#  GUI with dynamic UI for testing
#  Config file stored on server
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

import sys

from socket import gethostname
from os import path
from traceback import format_exc
from ctypes import windll

from lib.sequence_library import Sequence
from lib.logger_library import Logger
from lib.config_library import Config


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
            print(self.application_path.rsplit('\\', 1)[0] + '/config/'
                                             + gethostname() + '.ini')
            temp = Config.read_config(Config(self.application_path + '/config/'
                                             + gethostname() + '.ini'))
            print(temp)
        except FileNotFoundError:
            windll.user32.MessageBoxW(0, 'Error 0x100 Config file not found', 'Error', 0x1000)
            Logger.log_event(Logger(), 'Error 0x100 Config file not found. ' + format_exc())
            sys.exit()
        # TODO:
        #  Read config file and fill variables
        pass

    @staticmethod
    def test(self):
        # test procedure
        Sequence.sequence_read(Sequence('main.program'))
        pass

Main.test(Main())