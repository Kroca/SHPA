from Devices.Device import Device
from Util.Values import Values
from Util.HistoryLogger import HistoryLogger


class SensingDevice(Device):
    """Sensor class for device with singular integer value"""

    def __init__(self, sensorInfo):
        super(SensingDevice, self).__init__(sensorInfo['name'], sensorInfo['topic'])
        self.globalValues = Values()
        self.initValues()


    def initValues(self):
        """setup initial values for placeholder"""
        self.globalValues.setValue(self.name, 300)

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, msg):
        self._message = msg
        self.parseValues()

    def parseValues(self):
        """parsing message received from actual sensor"""
        self.globalValues.setValue(self.name, float(self.message))


class SensorDHT11(SensingDevice):
    """Sensor class for DHT11"""
    def __init__(self, sensorInfo):
        super(SensorDHT11, self).__init__(sensorInfo)

    def parseValues(self):
        tokens = self._message.split(" ")
        self.globalValues.setValue(tokens[0], tokens[1])
        self.globalValues.setValue(tokens[2], tokens[3])

    def initValues(self):
        self.globalValues.setValue("Temperature",22)
        self.globalValues.setValue("Humidity",40)


class PresenceSensor(SensingDevice):
    """Sensor class for Presence sensors"""
    def __init__(self, sensorInfo):
        self.logger = HistoryLogger()
        super(PresenceSensor, self).__init__(sensorInfo)

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
