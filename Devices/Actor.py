from abc import ABCMeta, abstractmethod, abstractproperty


class Actor(object):
    """Abstract class for any actor in a system"""
    __metaclass__ = ABCMeta

    def __init__(self):
        self._possibleActions = {}
        self._possibleStates = {}

    @abstractmethod
    def getName(self):
        return NotImplementedError

    def getAction(self,action_name):
        return NotImplementedError

    @property
    @abstractmethod
    def possibleActions(self):
        return self._possibleActions

    @possibleActions.setter
    @abstractmethod
    def possibleActions(self, value):
        self._possibleActions = value

    @property
    @abstractmethod
    def possibleStates(self):
        return self._possibleStates

    @possibleStates.setter
    @abstractmethod
    def possibleStates(self, value):
        self._possibleStates = value

    @property
    @abstractmethod
    def state_transactions(self):
        return self._state_transactions

    @state_transactions.setter
    @abstractmethod
    def state_transactions(self, value):
        self._state_transactions = value

    @property
    @abstractmethod
    def currentState(self):
        return self._currentState

    @currentState.setter
    @abstractmethod
    def currentState(self, value):
        self._currentState = value

    @abstractmethod
    def performAction(self, action, *args):
        return NotImplementedError

    @abstractmethod
    def getPossibleStatesList(self):
        return NotImplementedError

    @abstractmethod
    def is_possible(self,action):
        return NotImplementedError
