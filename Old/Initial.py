from flask import Flask, render_template
from flask import request
import webbrowser
import sys
import urllib
import paho.mqtt.client as mqtt
import urllib.request
import datetime

now = datetime.datetime.now()
app = Flask(__name__)
stopic = 'server'
temp = 21
light = 238
hum = 56
avgMinT = 22
avgTimeL = "18:33"
mqttc = mqtt.Client()
mqttc.connect("localhost",1883,60)
mqttc.subscribe(stopic)
with open('out.txt','r') as f:
    history = f.readlines()
# data = open('out.txt','r')
# history = data
# history.append('12-3012odsads')
# def on_connect(client,userdata,rc):
# 	client.subscribe(stopic)
# history = ["line1","line2","line3"]
def on_message(client,userdata,msg):
	global hum,temp,light,history,now
	time = now.strftime("%d-%m-%Y %H:%M") + " "
	tempString = msg.payload.decode()
	splits = tempString.split(' ')
	temp = splits[0]
	light = splits[2]
	hum = splits[1]
	history.append(time + tempString)


# mqttc.on_connect = on_connect
mqttc.on_message = on_message

mqttc.loop_start()
# mqttc.subscribe(stopic)



pins = { 4: {'name':'Heater','board':'esp8266','topic':'esp8266/4','state':'False'},
		 5: {'name':'Light','board':'esp8266','topic':'esp8266/5','state':'False'},
		 6: {'name':'Humidifier','board':'esp8266','topic':'esp8266/6','state':'False'}}
templateData = {'pins':pins}
@app.route("/")
def main():
	return render_template('index.html',**templateData,temp = temp,light = light,hum = hum)
@app.route("/<board>/<chagePin>/<action>")
def action(board,chagePin,action):
	chagePin = int(chagePin)
	devicePin = pins[chagePin]['name']
	if action == "1" and board == "esp8266":
		mqttc.publish(pins[chagePin]['topic'],1)
		pins[chagePin]['state'] = 'True'
	if action == "0" and board == "esp8266":
		mqttc.publish(pins[chagePin]['topic'],0)
		pins[chagePin]['state'] = 'False'
	templateData = { 'pins' : pins }
	return render_template('index.html',**templateData,temp = temp,light = light,hum = hum)
@app.route("/ssad")
def ssad():
	try:
		lang = request.args.get('proglang', 0, type=str)
		if lang.lower() == 'python':
			return jsonify(result='You are wise')
		else:
			return jsonify(result='Try again.')
	except Exception as e:
		return str(e)
@app.route('/data')
def data():
	return render_template('data.html',history=history,avgMinT = avgMinT,avgTimeL = avgTimeL)

if __name__ == '__main__':
	app.run(debug=True , host='0.0.0.0')