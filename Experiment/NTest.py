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
# 	app.run(debug=True , host='0.0.0.0')