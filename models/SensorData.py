from sqlalchemy import Column, Integer, String, Date
from DAO.database import Base


class SensorData(Base):
    __tablename__ = 'sensordata'
    id = Column(Integer, primary_key=True)
    sensor_name = Column(String(50), unique=False)
    value = Column(String(50), unique=False)
    date = Column(Date, unique=False)

    def __init__(self, name=None, value=None,date = None):
        self.sensor_name = name
        self.value = value
        self.date = date

    def __repr__(self):
        return '<User %r value %r date %r>' % (self.sensor_name, self.value, self.date)
