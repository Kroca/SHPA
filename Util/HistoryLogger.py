from Util.Values import Singleton
import datetime


class HistoryLogger(object, metaclass=Singleton):
    def __init__(self):
        # read file with history
        print("init")

    def log(self, info):
        # add new line with log
        with open('out.txt', 'a') as f:
            msg = datetime.datetime.now().strftime("%d-%m-%Y %H:%M") + " " + info + "\n"
            print("printing message to log" + msg)
            f.write(msg)

    def getLog(self):
        with open('out.txt', 'r') as f:
            history = f.readlines()
            return history