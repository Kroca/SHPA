from Logic.Condition import Condition, ValueCondition, StateCondition
from Logic.Action import Action


class Scenario(object):
    """docstring for Scenario"""

    def __init__(self, name, description):
        super(Scenario, self).__init__()
        self._actionSet = []
        self.description = description
        self._conditions = []
        self.name = name
        # mark that system is already activated scenario, and there is no need to do it again
        # (when after this actions scenario is still true )
        self.active = False
        # mark if we want to check this scenario or we turned off for some time
        self.enabled = True

    def getDescription(self):
        return self.description

    def toggle(self,state):
        self.enabled = state

    def addAction(self, actor, action):
        self._actionSet.append(Action(actor, action))

    def addCondition(self, condition):
        self._conditions.append(condition)
        if type(condition) is ValueCondition:
            condition.setScenario(self)

    def checkConditionsSatisfaction(self):
        for condition in self._conditions:
            if not condition.isSatisfied():
                print(condition)
                return False
        return True

    def performScenario(self):
        if not self.enabled:
            return
        print("scenario is" + str(self.checkConditionsSatisfaction()))
        if self.checkConditionsSatisfaction():
            if not self.active:
                for action in self._actionSet:
                    action.perform()
                self.active = True
        else:
            self.active = False
