from DAO.database import init_db
from DAO.database import db_session
from models.SensorData import SensorData
import datetime

init_db()
sensor = SensorData("Light","10",datetime.datetime.now())
db_session.add(sensor)
db_session.commit()

print(SensorData.query.all())