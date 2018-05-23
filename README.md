# SHPA
Smart home personal assistant with focus on MQTT protocol.
It allows you to control your home automation and create custom scenarios.

#Installation
* First you need to setup an mqtt broker. (e.g Mosquitto <https://mosquitto.org/>)
* clone the project and install the requirements
```python
pip install -r requirements.txt
```
* run the app
```
python app.py
```
You can access it at localhost:5000
# Edit
You can edit the configuratios in actor/sensor and scenario files in DAO.
To add new sensor extend it from SesningDevice, to add new acting device extend it from Actor.

# Arduino support
Each sensor device has a topic by which he sends data to assistant.
Each actor subscribes to the topic by which he gets commands from assistant.
example of Arduino code is in repo.

