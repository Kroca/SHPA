from Devices.Device import Device
from enum import Enum
from Devices.Actor import Actor
import Logic.Assistant


class BinaryActingDevice(Device, Actor):
    class Actions(Enum):
        TURN_ON = "Turn on"
        TURN_OFF = "Turn off"

    class States(Enum):
        ON = 1
        OFF = 0

    """docstring for ActingDevice"""

    def __init__(self, name, topic):
        Device.__init__(self, name, topic)
        Actor.__init__(self)
        self.possibleActions = self.Actions
        self.possibleStates = self.States
        self.currentState = self.States.OFF
        # set of possible transactions that can be performed
        self.state_transactions = {self.possibleStates.ON: {self.possibleActions.TURN_OFF: self.possibleStates.OFF},
                                   self.possibleStates.OFF: {self.possibleActions.TURN_ON: self.possibleStates.ON}}

    def getCurrentState(self):
        return self.currentState.value

    def getName(self):
        return self.name

    def getPossibleStatesList(self):
        return list(map(lambda action: action.name, self.possibleActions))

    def performAction(self, action, *args):
        if action in self.state_transactions[self.currentState]:  # if following action is possible then
            # send mqtt request to device and wait for callback possible even send some params from *param
            newState = self.state_transactions[self.currentState][action]
            Logic.Assistant.sendMQTTMessage(self.topic, newState.value)
            self.currentState = newState
            info = self.name + " " + newState.name + "\n "
            Logic.Assistant.logger.log(info)

    def is_possible(self,action):
        return action in self.state_transactions[self.currentState]