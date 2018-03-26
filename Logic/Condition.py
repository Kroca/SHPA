from abc import ABCMeta, abstractmethod, abstractproperty
from Util.Values import Values
import datetime


class Condition(object):
    """Abstract class for any condition in a system"""
    __metaclass__ = ABCMeta

    @abstractmethod
    def isSatisfied(self):
        print("method is not defined")
        pass


class ValueCondition(Condition):
    """Condition class"""

    def __init__(self, json):
        super(ValueCondition, self).__init__()
        self._currentValue = Values().getValue(json['valueName'])
        self._operator = json['operator']
        self._comparisonValue = json['compareValue']


    def setScenario(self, scenario):
        self._scenario = scenario
        self._currentValue.subscribe(scenario)

    def getScenario(self):
        return self._scenario

    def isSatisfied(self):
        if self._operator == "<":
            if self._currentValue.value < self._comparisonValue:
                return True
            else:
                return False
        elif self._operator == ">":
            if self._currentValue.value > self._comparisonValue:
                return True
            else:
                return False
        elif self._operator == "=":
            if self._currentValue.value == self._comparisonValue:
                return True
            else:
                return False


class TimeCondition(Condition):
    """Time condition for the time based events"""
    def __init__(self, json):
        time = json['time'].split(":")
        if len(time) > 1:
            self.hour = int(time[0])
            self.minute = int(time[1])
        else:
            print("wrong time input")
        self.operator = json['operator']

    def isSatisfied(self):
        time = datetime.datetime.now()
        if self.operator == "<":
            return (self.hour * 60 + self.minute) < time.hour * 60 + time.minute
        elif self.operator == ">":
            return (self.hour * 60 + self.minute) > time.hour * 60 + time.minute
        else:
            return False


class StateCondition(Condition):
    """State condition for controlling actuators based on current state of actuator"""

    def __init__(self, json):
        self._actor = json['actor']
        self._desiredState = json['desiredState']

    def isSatisfied(self):
        if self._actor.currentState == self._desiredState:
            return True
        else:
            return False
