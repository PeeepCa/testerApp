# Logger library

from datetime import datetime


class Logger:
    """
    Library for logging. Logged in directory as txt file named as date.
    """
    def __init__(self):
        self.config = open(Logger.time_stamp().split(' ')[0].replace('.', '') + '_log.txt', 'a')

    @staticmethod
    def time_stamp():
        """
        Timestamp
        :return: actual_time
        """
        actual_time = datetime.now()
        actual_time = actual_time.strftime('%d.%m.%Y %H:%M:%S')
        return str(actual_time)

    def log_event(self, content):
        """
        Log event, write data to log file.
        :param content: What to write to log file.
        """
        self.config.write(Logger.time_stamp() + ': ' + content + '\n')
        self.config.close()
