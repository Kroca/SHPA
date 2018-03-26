from Logic.Scenario import Scenario
from Devices.ActingDevice import BinaryActingDevice
from DAO.database import init_db
import json


class Storage(object):
    def __init__(self):
        init_db()
        self._sensingDevices = []
        self._scenarios = []
        self._actingDevices = []
        self.load()

    def load(self):
        # deserialize
        # getting sensor data
        sensors = json.load(open("DAO/sensors"))
        for sensor in sensors:
            cls = self.get_class("Devices.SensingDevice." + sensor['class_name'])
            self._sensingDevices.append(cls(sensor['name'], sensor['topic']))

        # getting actor data
        actors = json.load(open("DAO/actors"))
        for actor in actors:
            cls = self.get_class("Devices.ActingDevice." + actor['class_name'])
            self._actingDevices.append(cls(actor['name'],actor['topic']))

        scenarios = json.load(open("DAO/scenarios"))
        for scenario in scenarios:
            sc = Scenario(scenario['name'],scenario['description'])
            for action in scenario['actions']:
                actor = self.getActor(action['actor'])
                t_action = actor.getAction(action['action'])
                sc.addAction(actor,t_action)
            for condition in scenario['conditions']:
                cls = self.get_class("Logic.Condition."+condition['type'])
                t_c = cls(condition)
                sc.addCondition(t_c)
            self._scenarios.append(sc)

    def get_class(self, kls):
        parts = kls.split('.')
        module = ".".join(parts[:-1])
        m = __import__(module)
        for comp in parts[1:]:
            m = getattr(m, comp)
        return m

    # def tempInintDevice(self):
        # sensors
        # s_light = SensingDevice("Light", "sensorData/light")
        # s_light.message = "230"
        #
        # s_dht = SensorDHT11("DHT11", "sensorData/dht11")
        # s_dht.message = "Temperature 30 Humidity 64"
        #
        # s_presence = PresenceSensor("Presence", "sensorData/PIR")
        # s_presence.message = "1"
        #
        # # actuator
        # a_light = BinaryActingDevice("LightControl", "actuators/light")
        #
        # # scenarios
        # light_scenario = Scenario("LightingScenario", "Turn on the light at dark if someone is in room")
        # light_scenario.addAction(a_light, a_light.Actions.TURN_ON)
        # light_scenario.addCondition(TimeCondition("23:00", "<"))
        # light_scenario.addCondition(ValueCondition("Light", ">", 200))
        # # todo check this on raspberry settings
        # light_scenario.addCondition(ValueCondition("Presence", "=", 0))
        #
        # # append
        # self._sensingDevices.append(s_light)
        # self._sensingDevices.append(s_dht)
        # self._actingDevices.append(a_light)
        # self._sensingDevices.append(s_presence)
        # self._scenarios.append(light_scenario)

    def getScenarios(self):
        return self._scenarios

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

    def getScenario(self, scenario_name):
        for scenario in self._scenarios:
            if scenario.name == scenario_name:
                return scenario
