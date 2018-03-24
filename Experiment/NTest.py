# from enum import Enum
# class Actions(Enum):
#     TURN_ON = "Turn on"
#     TURN_OFF = "Turn off"
# class States(Enum):
#     ON = "ON"
#     OFF = "OFF"

# actions = Actions
# states = States
# transactions = {states.ON:{actions.TURN_OFF:states.OFF},
#                 states.OFF:{actions.TURN_ON:states.ON}}

# if(actions.TURN_OFF in transactions[states.ON]):
#     print("jasjdajs")            
# # print(transactions[states.ON][actions.TURN_OFF])
from Assistant import Assistant
from Values import Values
from Condition import ValueCondition,EventCondition
# from flask import Flask, render_template
# app = Flask(__name__)

# @app.route("/")
# def main():
# 	return render_template('index.html')
test = []
print( len(test))

# assistant = Assistant()

# # testing sensing devices
assistant.addSensingDevice("Light","home/sensorData",60)
assistant.addSensingDevice("Temperature", "home/sensorData",60)
assistant.getSensingDevices()[0].message = "220"
tempSensor = assistant.getSensingDevices()[1]
tempSensor.message = "10"
print(assistant.getSensingDevices()[0].name)
print(Values().getValue("Light"))

# #testing acting devices
assistant.addActingDevice("Light control relat","home/actuators")
actor = assistant.getActingDevices()[0]
print(actor.currentState)
actor.performAction(actor.possibleActions.TURN_ON)
print(actor.currentState)
assistant.addScenario(actor,actor.possibleActions.TURN_OFF)
scenario = assistant.getScenarios()[0]
valueCond = ValueCondition("Light","<",250)
scenario.addCondition(valueCond)
valueCond2  = ValueCondition("Temperature",">",20)
scenario.addCondition(valueCond2)
print(scenario.checkConditionsSatisfaction())
tempSensor.message = "30"
# if __name__ == '__main__':
# 	app.run(debug=True , host='0.0.0.0')