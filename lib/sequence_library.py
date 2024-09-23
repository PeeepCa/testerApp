from lib.itac_library import Itac
from lib.logger_library import Logger
from ctypes import windll
from traceback import format_exc


class Sequence:
    """
    Calling the sequence file to process it.
    :param file: path to the sequence file
    """
    def __init__(self, file):
        file = open(file, 'r')
        self.sequence_file = file.read(-1).splitlines()
        file.close()

    def sequence_read(self):
        """
        Process the sequence file.
        """
        try:
            for sequence_step in self.sequence_file:
                print(sequence_step)
                match sequence_step.split('.')[0]:
                    case '1':
                        print('1')
                    case '2':
                        print('2')
                    case '3':
                        print('3')
                    case '4':
                        print('4')
                    case '5':
                        print('5')
                    case '6':
                        print('6')
                    case 'ITAC':
                        match sequence_step.split('.')[1]:
                            case 'LOGIN':
                                print(Itac.login(Itac('40010011', 'http://acz-itac/mes/imsapi/rest/actions/')))
                                print('LOGIN DONE')
                            case 'LOGOUT':
                                print(Itac.logout(Itac('40010011', 'http://acz-itac/mes/imsapi/rest/actions/')))
                                print('LOGOUT DONE')

        except (Exception, BaseException):
            windll.user32.MessageBoxW(0, 'Error 0x100 Undefined error in sequence call.' + format_exc(), 'Error', 0x1000)
            Logger.log_event(Logger(), 'Error 0x100 Undefined error in sequence call. ' + format_exc())

