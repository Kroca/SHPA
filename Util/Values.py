from DAO.database import db_session
from models.SensorData import SensorData
from datetime import datetime

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Values(object, metaclass=Singleton):
    """
    Static holder for all public Variables like Temperature/Humidity/Time etc.
    Only current values are stored.
    """

    def __init__(self):
        """
        :param self._valuesDict : dictionary of values
        """
        super(Values, self).__init__()
        self._valuesDict = {}

    def getVals(self):
        return self._valuesDict

    def setValue(self, valName, val, visibility=True, typeName=""):
        """
        :param valName: (String) name of the values by which it going to be searched and shown in system
        :param val: (Generic) actual value of the variable
        :param visibility: (Boolean) specifies if the value is going to be visible on front end along with others(remove?)
        :param typeName: type name of variable
        """
        # add param to specify if i should write the value to the database??
        # db_session.add(SensorData(valName, val, datetime.now()))
        # db_session.commit()
        # db_session.remove()
        if valName in self._valuesDict.keys():
            self._valuesDict[valName].value = val
        else:
            self._valuesDict[valName] = Value(val, visibility, typeName)

    def getValue(self, valName):
        if valName in self._valuesDict.keys():
            return self._valuesDict[valName]
        else:
            return None


class Value(object):
    def __init__(self, value, visible=True, typeName=""):
        super(Value, self).__init__()
        self._value = value
        self._visible = visible
        self._typeName = typeName
        self._subscribers = []

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value
        self.notify()

    @property
    def visible(self):
        return self._visible

    @property
    def typeName(self):
        return self._typeName

    @typeName.setter
    def typeName(self, value):
        self._typeName = value

    def subscribe(self, scenario):
        if scenario not in self._subscribers:
            self._subscribers.append(scenario)

    def notify(self):
        print("value with number of subscribers" + str(len(self._subscribers)))
        for subscriber in self._subscribers:
            subscriber.performScenario()
