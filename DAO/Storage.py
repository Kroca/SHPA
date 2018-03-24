from Devices.ActingDevice import BinaryActingDevice
from Devices.SensingDevice import SensingDevice, SensorDHT11, PresenceSensor
from Logic.Scenario import Scenario
from Logic.Condition import Condition, ValueCondition, StateCondition, TimeCondition


class Storage(object):
    def __init__(self):
        self._sensingDevices = []
        self._scenarios = []
        self._actingDevices = []
        self.load()

    def load(self):
        # deserialize
        self.tempInintDevice()

    def save(self):
        # serialize
        pass

    def tempInintDevice(self):
        # sensors
        s_light = SensingDevice("Light", "sensorData/light", 60)
        s_light.message = "230"

        s_dht = SensorDHT11("DHT11", "sensorData/dht11", 60)
        s_dht.message = "Temperature 30 Humidity 64"

        s_presence = PresenceSensor("Presence", "sensorData/PIR", -1)
        s_presence.message = "1"

        # actuator
        a_light = BinaryActingDevice("LightControl", "actuators/light")

        # scenarios
        light_scenario = Scenario("LightingScenario", "Turn on the light at dark if someone is in room")
        light_scenario.addAction(a_light, a_light.Actions.TURN_ON)
        light_scenario.addCondition(TimeCondition("23:00", "<"))
        light_scenario.addCondition(ValueCondition("Light", ">", 200))
        light_scenario.addCondition(ValueCondition("Presence", "=", 0))

        # append
        self._sensingDevices.append(s_light)
        self._sensingDevices.append(s_dht)
        self._actingDevices.append(a_light)
        self._sensingDevices.append(s_presence)
        self._scenarios.append(light_scenario)

    def addScenario(self, scenario):
        self._scenarios.append(scenario)

    def getScenarios(self):
        return self._scenarios

    def addSensingDevice(self, name, topic, refreshRate):
        self._sensingDevices.append(SensingDevice(name, topic, refreshRate))

    def addActingDevice(self, name, topic):
        self._actingDevices.append(BinaryActingDevice(name, topic))

    def getSensingDevices(self):
        return self._sensingDevices

    def getActingDevices(self):
        return self._actingDevices

    def getActor(self, actor_name):
        for actor in self._actingDevices:
            if actor.getName() == actor_name:
                return actor

    def getSensor(self, sensor_name):
        for sensor in self._sensingDevices:
            if sensor.name == sensor_name:
                return sensor

    def getScenario(self,scenario_name):
        for scenario in self._scenarios:
            if scenario.name == scenario_name:
                return scenario
