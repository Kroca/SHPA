from Devices.Actor import Actor
from enum import Enum


class Thermostat(Actor):

    class Actions(Enum):
        SET_TEMPERATURE = "Set temperature"
        TURN_OFF = "Turn off"

    class States(Enum):
        ON = 1
        OFF = 0

    def performAction(self, action, *args):
        print(action, args)

    def __init__(self, name):
        Actor.__init__(self, name)
        self.possibleActions = self.Actions
        self.possibleStates = self.States


thermostat = Thermostat("termometer")
thermostat.performAction(thermostat.Actions.SET_TEMPERATURE)