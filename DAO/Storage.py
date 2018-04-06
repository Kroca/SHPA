from Logic.Scenario import Scenario
from Devices.ActingDevice import BinaryActingDevice
from DAO.database import init_db
from Devices.MusicActor import MusicPlayer
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

        self._actingDevices.append(MusicPlayer())
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

    def reload(self):
        self._scenarios = []
        self._sensingDevices = []
        self._actingDevices = []
        self.load()

    def get_class(self, kls):
        parts = kls.split('.')
        module = ".".join(parts[:-1])
        m = __import__(module)
        for comp in parts[1:]:
            m = getattr(m, comp)
        return m

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
