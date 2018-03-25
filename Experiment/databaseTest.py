from DAO.database import init_db
from DAO.database import db_session,engine
from models.SensorData import SensorData
import datetime

# init_db()
# SensorData.__table__.drop(engine)
# sensor = SensorData("Light","10",datetime.datetime.now())
# db_session.add(sensor)
# db_session.commit()

print(SensorData.query.all())