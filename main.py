# error 0x000 Main error
# error 0x100 UI error
# error 0x200 Sequence error
# error 0x300 itac error
# error 0x400 seso error
# error 0x500 rs232 error
# error 0x600 lan error


# TODO:
#  ** Multithreading for parallel testing - Done
#  ** GUI with dynamic UI for testing - Partially
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
#  ** Results implementation - Done
#  ** Results handling - Done

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
        lib.shared_variables.application_path = self.application_path
        self.sequence = Sequence()
        self.parsed_data = None

    def run_sequence(self):
        try:
            while not lib.shared_variables.app_exit:
                with lib.shared_variables.shared_condition:
                    if lib.shared_variables.program_status is not None and lib.shared_variables.sequence_file is not None:
                        match lib.shared_variables.program_status:
                            case 'PREUUT':
                                self.preuut()
                            case 'SEQUENCE':
                                self.main_sequence()
                            case 'POSTUUT':
                                self.postuut()
                    elif lib.shared_variables.sequence_file is None and lib.shared_variables.program_status == 'POSTUUT':
                        self.postuut()
                    else:
                        lib.shared_variables.shared_condition.wait()
        except Exception as e:
            self.logger.log_event('Error 0x000 ' + str(e))

    def preuut(self):
        try:
            self.parsed_data = self.sequence.parse_sequence_file(lib.shared_variables.sequence_file)
            self.sequence.sequence_read(self.parsed_data[0], self.parsed_data[1][0], self.parsed_data[1][1], 1)
            self.sequence.sequence_read(self.parsed_data[0], self.parsed_data[2][0], self.parsed_data[2][1], 1)
            lib.shared_variables.program_status = None
            lib.shared_variables.result_list.clear()
        except FileNotFoundError:
            # if you cancel the open file dialog
            pass

    def main_sequence(self):
        while lib.shared_variables.main_run:
            self.sequence.sequence_read(self.parsed_data[0], self.parsed_data[3][0], self.parsed_data[3][1], 1)

    def postuut(self):
        if lib.shared_variables.sequence_file is not None:
            self.sequence.sequence_read(self.parsed_data[0], self.parsed_data[4][0], self.parsed_data[4][1], 1)
        lib.shared_variables.program_status = None
        lib.shared_variables.result_list.clear()
        lib.shared_variables.app_exit = True

    @staticmethod
    def run_ui():
        UI.run(UI())

    def run(self):
        t0 = Thread(target=App.run_ui)
        t0.start()
        t1 = Thread(target=self.run_sequence)
        t1.start()
        t0.join()  # Wait for UI thread to finish
        t1.join()  # Wait for sequence thread to finish
        self.logger.log_event('Application exited successfully.')

if __name__ == "__main__":
    app = App()
    app.run()