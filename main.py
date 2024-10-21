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
import lib.shared_variables

from os import path
from threading import Thread

from lib.sequence_library import Sequence
from lib.logger_library import Logger
from lib.ui import UI


class App:
    def __init__(self):
        self.logger = Logger()
        self.logger.log_event('Logging started.')
        if getattr(sys, 'frozen', False):
            self.application_path = path.dirname(sys.executable)
        elif __file__:
            self.application_path = path.dirname(__file__)
        else:
            self.application_path = None
        self.sequence = Sequence()
        self.parsed_data = None

    def run_sequence(self):
        while not lib.shared_variables.app_exit:
            match lib.shared_variables.program_status:
                case 'PREUUT':
                    self.preuut()
                case 'SEQUENCE':
                    self.main_sequence()
                case 'POSTUUT':
                    self.postuut()

    def preuut(self):
        self.parsed_data = self.sequence.parse_sequence_file(lib.shared_variables.sequence_file)
        self.sequence.sequence_read(self.parsed_data[0], self.parsed_data[1][0], self.parsed_data[1][1], 1)
        self.sequence.sequence_read(self.parsed_data[0], self.parsed_data[2][0], self.parsed_data[2][1], 1)
        lib.shared_variables.program_status = None

    def main_sequence(self):
        while lib.shared_variables.main_run:
            self.sequence.sequence_read(self.parsed_data[0], self.parsed_data[3][0], self.parsed_data[3][1], 1)

    def postuut(self):
        self.sequence.sequence_read(self.parsed_data[0], self.parsed_data[4][0], self.parsed_data[4][1], 1)
        lib.shared_variables.program_status = None
        lib.shared_variables.app_exit = True

    @staticmethod
    def run_ui():
        UI.run(UI())

    def run(self):
        t0 = Thread(target=App.run_ui)
        t0.start()
        t1 = Thread(target=self.run_sequence)
        t1.start()

if __name__ == "__main__":
    app = App()
    app.run()