from lib.itac_library import Itac


class Sequence:
    def __init__(self, file):
        self.sequence_file = file
        file = open(file, 'r')
        self.sequence_file = file.read(-1).splitlines()
        file.close()

    def sequence_read(self):
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
                    temp = sequence_step.split('.')[1]
                    print(temp)
                    match temp:
                        case 'LOGIN':
                            print(Itac.login(Itac('40010011', 'http://acz-itac/mes/imsapi/rest/actions/')))
                            print('LOGIN DONE')
                        case 'LOGOUT':
                            Itac.logout(Itac('40010011', 'http://acz-itac/mes/imsapi/rest/actions/'))
                            print('LOGOUT DONE')


Sequence.sequence_read(Sequence('main.program'))
