from Logic.MQTTManager import MQTTManager
from DAO.Storage import Storage
from Util.HistoryLogger import HistoryLogger
from Util.Values import Values

mqttManager = MQTTManager()
logger = HistoryLogger()
mqttManager.start()
storage = Storage()
values = Values()


def sendMQTTMessage(topic, message):
    mqttManager.getClient().publish(topic, message)


def getScenarios():
    """return list of scenarios"""
    return storage.getScenarios()


def getSensors():
    """return list of sensors"""
    return storage.getSensingDevices()


def getActors():
    """return list of actors"""
    return storage.getActingDevices()


def getActor(actor_name):
    """return particular actor by name"""
    return storage.getActor(actor_name)


def getSensor(sensor_name):
    """:return particular sensor by name"""
    return storage.getSensor(sensor_name)


def getValues():
    """:return list of value in the system"""
    return values.getVals()


def getValue(name):
    """:return particular value specified by name """
    return values.getValue(name)


def getScenario(scenario_name):
    """:return particular scenario by name"""
    return storage.getScenario(scenario_name)


def performAction(actor, action, *args):
    """
    :param actor : specifies name of the actor that should perform an action
    :param action :  specifies name of the action
    """
    thisActor = getActor(actor)
    thisActor.performAction(thisActor.getAction(action), args)


def toggleScenario(scenario_name, state):
    """
    :param scenario_name: name of the scenario that you want to toggle
    :param state: boolean specifying the state ( True-ON / False- OFF)
    """
    getScenario(scenario_name).toggle(state)


def editScenario(type, params, scenario):
    # this one is optional really
    pass
