from Util.Values import Singleton
import datetime


class HistoryLogger(object, metaclass=Singleton):
    def __init__(self):
        # read file with history
        self.now = datetime.datetime.now()

    def log(self, info):
        # add new line with log
        with open('out.txt', 'a') as f:
            msg = self.now.strftime("%d-%m-%Y %H:%M") + " " + info + "\n"
            print("printing message to log" + msg)
            f.write(msg)

    def getLog(self):
        with open('out.txt', 'r') as f:
            history = f.readlines()
            return history
