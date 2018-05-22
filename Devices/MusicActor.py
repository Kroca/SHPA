from Devices.Actor import Actor
from enum import Enum
from clementineremote import ClementineRemote
import Logic.Assistant

class MusicPlayer(Actor):
    """Example of software actor"""
    def __init__(self):
        self.name = "Music Player"
        super().__init__()
        self.possibleActions = self.Actions
        self.possibleStates = self.States
        self.currentState = self.States.STOPPED
        self.state_transactions = {}
        try:
            self.clementine = ClementineRemote(host="localhost", port=5500, auth_code=None)
        except:
            Logic.Assistant.logger.log("couldn't connect to Clementine")


        
    def getName(self):
        return self.name

    def performAction(self, action, *args):
        if not self.is_connected():
            return

        if action == self.Actions.PLAY:
            self.clementine.play()
            self.currentState = self.States.PLAYING

        if action == self.Actions.NEXT:
            self.clementine.next()
            self.currentState = self.States.PLAYING

        if action == self.Actions.PREVIOUS:
            self.clementine.previous()
            self.currentState = self.States.PLAYING

        if action == self.Actions.STOP:
            self.clementine.stop()
            self.currentState = self.States.STOPPED

        if action == self.Actions.PAUSE:
            self.clementine.pause()
            self.currentState = self.States.STOPPED
        # not implemented on front yet
        if action == self.Actions.SET_VOLUME:
            self.clementine.set_volume(args[0]['volume'])

        info = self.name + " action " + action.value +" \n"
        Logic.Assistant.logger.log(info)


    def getPossibleStatesList(self):
        pass

    def is_possible(self, action):
        pass

    class Actions(Enum):
        PLAY = "Play"
        STOP = "Stop"
        PAUSE = "Pause"
        NEXT = "Next"
        PREVIOUS = "Previous"
        SET_VOLUME = "Set volume"

    class States(Enum):
        PLAYING = 1
        STOPPED = 0

    def is_connected(self):
        return self.clementine.first_data_sent_complete

