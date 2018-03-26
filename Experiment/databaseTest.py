# from DAO.database import init_db
# from DAO.database import db_session,engine
# from models.SensorData import SensorData
# import datetime

# init_db()
# SensorData.__table__.drop(engine)
# sensor = SensorData("Light","10",datetime.datetime.now())
# db_session.add(sensor)
# db_session.commit()

# print(SensorData.query.all())
# ------------------------------------------------------
# def get_class(kls):
#     parts = kls.split('.')
#     module = ".".join(parts[:-1])
#     m = __import__(module)
#     for comp in parts[1:]:
#         m = getattr(m, comp)
#     return m


# obj = get_class("Devices.SensingDevice.SensingDevice")
# sensingDevice = obj("Light", "sensor")
# -------------------------------------------------------
# sensor = SensingDevice("Light", "sensorData/light")
from Devices.SensingDevice import SensingDevice,PresenceSensor
import json

data = json.load(open("DAO/scenarios"))
print(data[0]['conditions'][0].items())

