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
#  Error handling inside the APP - Done
#  iTAC via restAPI
#  SESO via restAPI
#  ** HW library - rs232 done with timeout which need to be defined
#  Muster
#  ** Sequence implementation for testing - Done
#  Selftest for relay cards
#  Relay control from tab in app

import sys

from os import path

from lib.sequence_library import Sequence
from lib.logger_library import Logger


class Main:
    def __init__(self):
        Logger.log_event(Logger(), 'Logging started.')
        if getattr(sys, 'frozen', False):
            self.application_path = path.dirname(sys.executable)
        elif __file__:
            self.application_path = path.dirname(__file__)
        else:
            self.application_path = None

    @staticmethod
    def test(__):
        """
        Test function
        :param __:
        :return:
        """
        # test procedure
        Sequence.settings_read(Sequence('sequence.csv', 1))
        Sequence.preuut_read(Sequence('sequence.csv', 1))
        Sequence.sequence_read(Sequence('sequence.csv', 1))
        Sequence.postuut_read(Sequence('sequence.csv', 1))

Main.test(Main())