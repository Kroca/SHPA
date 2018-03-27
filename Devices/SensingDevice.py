from Devices.Device import Device
from Util.Values import Values
from Util.HistoryLogger import HistoryLogger


class SensingDevice(Device):
    """docstring for SensingDevice"""

    def __init__(self, name, topic):
        super(SensingDevice, self).__init__(name, topic)
        self.globalValues = Values()
        self.initValues()

    def initValues(self):
        self.globalValues.setValue(self.name, 0)

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, msg):
        self._message = msg
        self.parseValues()

    def parseValues(self):
        self.globalValues.setValue(self.name, float(self.message))


class SensorDHT11(SensingDevice):

    def __init__(self, name, topic):
        super(SensorDHT11, self).__init__(name, topic)

    def parseValues(self):
        tokens = self._message.split(" ")
        self.globalValues.setValue(tokens[0], tokens[1])
        self.globalValues.setValue(tokens[2], tokens[3])

    def initValues(self):
        self.globalValues.setValue("Temperature",0)
        self.globalValues.setValue("Humidity",0)


class PresenceSensor(SensingDevice):

    def __init__(self, name, topic):
        self.logger = HistoryLogger()
        super(PresenceSensor, self).__init__(name, topic)

    def initValues(self):
        self.globalValues.setValue(self.name,"Absent",False)

    def parseValues(self):
        log_msg = ""
        if int(self.message) == 1:
            log_msg = "Present"
        elif int(self.message) == 0:
            log_msg = "Absent"
        self.globalValues.setValue(self.name, log_msg, False)
        log_msg = self.name + log_msg
        self.logger.log(log_msg)
