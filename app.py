from flask import Flask, render_template, request, jsonify
import Logic.Assistant as Assistant
from Util import Values

app = Flask(__name__)


sensors = values.getVals()
actuators = Assistant.storage.getActingDevices()
scenarios = Assistant.storage.getScenarios()


@app.route("/")
def main():
    return render_template('index.html', sensors=sensors, actuators=actuators)


@app.route("/process", methods=['POST'])
def process():
    checkbox = request.get_json(force=True)
    actor = actuators[0]
    print("button switch state")
    if checkbox['state']:
        actor.performAction(actor.possibleActions.TURN_ON)
    else:
        actor.performAction(actor.possibleActions.TURN_OFF)
    print("current state is ")
    scenarios[0].performScenario()
    return ""


@app.route('/handle_data', methods=['POST'])
def handle_data():
    # projectpath = request.form['projectFilepath']
    result = request.form
    print("this should not be called")
    return ""


@app.route("/updateSensors")
def updateSensors():
    temp = values.getValue("Temperature").value
    hum = values.getValue("Humidity").value
    light = values.getValue("Light").value
    return jsonify(temp=temp, hum=hum, light=light)


@app.route('/settings')
def settings():

    # print(values.getVals().keys())
    return render_template('settings.html',
                           scenarios=scenarios,
                           values=values.getVals(),
                           actors=actuators)


@app.route("/history")
def history():
    print("Showing history")
    return render_template('history.html', history=Assistant.logger.getLog())

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',use_reloader=False)
