from flask import Flask, render_template, request, jsonify
from Logic import Assistant
from Util import Values

app = Flask(__name__)

sensors = Assistant.getValues()
actuators = Assistant.getActors()
scenarios = Assistant.getScenarios()


@app.route("/")
def main():
    return render_template('index.html', assistant=Assistant)


@app.route("/performAction", methods=['POST'])
def performAction():
    json_req = request.get_json(force=True)
    print(json_req['actor_name'])
    try:
        actor = Assistant.getActor(json_req['actor_name'])
        action = actor.getAction(json_req['action_name'])
        print(actor)
        print(action)
        actor.performAction(action)
        return "Success"
    except:
        return "Failed to perform the action"


@app.route('/toggle_scenario', methods=['POST'])
def toggle_scenario():
    json_req = request.get_json(force=True)
    scenario_to_edit = Assistant.getScenario(json_req['scenario_name'])
    scenario_to_edit.toggle(json_req['state'])
    print(scenario_to_edit.enabled)
    return ""


@app.route("/updateSensors")
def updateSensors():
    """temporarily used for updating sensor data on front
    :return json with some sensor data"""
    temp = Assistant.getValue("Temperature").value
    hum = Assistant.getValue("Humidity").value
    light = Assistant.getValue("Light").value
    return jsonify(temp=temp, hum=hum, light=light)


@app.route('/settings')
def settings():
    # print(values.getVals().keys())
    return render_template('settings.html',
                           scenarios=scenarios,
                           values=sensors,
                           actors=actuators)


@app.route('/reload', methods=['POST'])
def reload():
    Assistant.storage.reload()
    return ""


@app.route("/history")
def history():
    print("Showing history")
    return render_template('history.html', history=Assistant.logger.getLog())


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', use_reloader=False)
