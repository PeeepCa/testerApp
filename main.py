# TODO:
#  ** Multithreading for parallel testing - Done
#  GUI with dynamic UI for testing
#  ** Config file stored on server - Done
#  Auto updating like PEPO
#  ** Logging to server log file - reused from PEPO
#  ** Error handling inside the APP - Done
#  ** iTAC via restAPI - Done
#  SESO via restAPI
#  ** HW library - rs232 done with timeout which need to be defined
#  Muster
#  ** Sequence implementation for testing - Done
#  Selftest for relay cards
#  Relay control from tab in app
#  Results implementation
#  Results handling

import sys

from os import path
from threading import Thread

from lib.sequence_library import Sequence
from lib.logger_library import Logger
from lib.ui import UI


class App:
    def __init__(self):
        Logger.log_event(Logger(), 'Logging started.')
        if getattr(sys, 'frozen', False):
            self.application_path = path.dirname(sys.executable)
        elif __file__:
            self.application_path = path.dirname(__file__)
        else:
            self.application_path = None
        self.sequence = Sequence()

    def test(self):
        """
        Test function
        :return:
        """
        # test procedure
        parsed = self.sequence.parse_sequence_file('sequence.csv')
        # Settings
        self.sequence.sequence_read(parsed[0], parsed[1][0], parsed[1][1], 1)
        # Preuut
        self.sequence.sequence_read(parsed[0], parsed[2][0], parsed[2][1], 1)
        # Sequence
        self.sequence.sequence_read(parsed[0], parsed[3][0], parsed[3][1], 1)
        # Postuut
        self.sequence.sequence_read(parsed[0], parsed[4][0], parsed[4][1], 1)

    @staticmethod
    def run_ui():
        UI.run(UI())

    def run_test(self):
        self.test()

    def run(self):
        t0 = Thread(target=App.run_ui)
        t0.start()
        t1 = Thread(target=App.run_test, args=(self,))
        t1.start()

if __name__ == "__main__":
    app = App()
    app.run()