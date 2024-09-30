# TesterAPP

# Error list:
# 0x000 Undefined error in main.
# 0x100 Undefined error in sequence call.
# 0x101 Undefined error in settings call.
# 0x200 Undefined error in rs232 call.

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
        parsed = Sequence.parse_sequence_file(Sequence('sequence.csv', 1))
        # Settings
        Sequence.settings_read(Sequence('sequence.csv', 1),parsed[0], parsed[1])
        # Preuut
        Sequence.sequence_read(Sequence('sequence.csv', 1),parsed[2], parsed[3])
        # Sequence
        Sequence.sequence_read(Sequence('sequence.csv', 1),parsed[4], parsed[5])
        # Postuut
        Sequence.sequence_read(Sequence('sequence.csv', 1),parsed[6], parsed[7])

Main.test(Main())