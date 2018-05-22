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
        action = actor.getAction(str.upper(json_req['action_name']))
        actor.performAction(action, json_req)
        map = {"answer": {"message_key": "{}".format(json_req['action_name']),
                          "message": "{} {}".format(json_req['actor_name'], action.value)}}
        return jsonify(map)
    except:
        map = {"error": {"message_key": "turn_on"}, "message": "error occurred"}
        return jsonify(map)


@app.route('/toggle_scenario', methods=['POST'])
def toggle_scenario():
    json_req = request.get_json(force=True)
    scenario_to_edit = Assistant.getScenario(json_req['scenario_name'])
    scenario_to_edit.toggle(json_req['state'])
    print(scenario_to_edit.enabled)
    return ""


@app.route("/getSensorsData", methods=['POST'])
def getSensorData():
    temp = Assistant.getValue("Temperature").value
    hum = Assistant.getValue("Humidity").value
    light = Assistant.getValue("Light").value
    map = {"answer": {"message_key": "dashboard",
                      "message": "Temperature {}, Humidity {}, Light {}".format(temp, hum, light)}}
    return jsonify(map)


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
