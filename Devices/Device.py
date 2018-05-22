from abc import ABCMeta, abstractmethod, abstractproperty


class Device(object):
    """Abstract class for any device in a system, must have a name and topic to which actual device publishes
    messages """

    __metaclass__ = ABCMeta

    def __init__(self, name, topic):
        self._name = name
        self.topic = topic

    @property
    @abstractmethod
    def name(self):
        return self._name

    @name.setter
    @abstractmethod
    def name(self, value):
        self._name = value

    @property
    @abstractmethod
    def topic(self):
        return self._topic

    @topic.setter
    @abstractmethod
    def topic(self, value):
        self._topic = value
