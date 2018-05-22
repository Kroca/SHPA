import paho.mqtt.client as mqtt
import Logic.Assistant

class MQTTManager(object):
    """MQTT manager for message passing"""

    def __init__(self):
        super(MQTTManager, self).__init__()

    # callback function that is executed when message received
    def on_message(self, client, userdata, msg):
        message = msg.payload.decode()
        for sensor in Logic.Assistant.getSensors():
            if sensor.topic == msg.topic:
                sensor.message = message
        return message

    def start(self):
        self.mqttc = mqtt.Client()
        self.mqttc.connect("localhost", 1883, 60)
        self.mqttc.subscribe("sensorData/#")
        self.mqttc.on_message = self.on_message
        self.mqttc.loop_start()

    def getClient(self):
        return self.mqttc
