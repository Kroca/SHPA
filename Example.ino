#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <SimpleDHT.h>

// Change the credentials below, so your ESP8266 connects to your router
const char* ssid = "ssid";
const char* password = "password";
// ip address of mqtt broker
const char* mqtt_server = "ip.address";

char msg[50];
WiFiClient espClient;
PubSubClient client(espClient);
//marker for pir sensor
byte prevState=0;
//marker of last message
long lastMsg = 0;
//pin for PIR sensor
const int pirMotionPin = 4;
//pin for relay
const int relePin = 5;
//pin for dht11
const int dhtPin = 0;
SimpleDHT11 dht11;
//delay between messages
const int dataTransimissionDelay = 300000;


// setting up wifi connection.
void setup_wifi() {
  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("WiFi connected - ESP IP address: ");
  Serial.println(WiFi.localIP());
}

// This functions is executed when assistant publishes a message to a topic that your ESP8266 is subscribed to
void callback(String topic, byte* message, unsigned int length) {
  Serial.print("Message arrived on topic: ");
  Serial.print(topic);
  Serial.print(". Message: ");
  String messageTemp;

  for (int i = 0; i < length; i++) {
    Serial.print((char)message[i]);
    messageTemp += (char)message[i];
  }
  Serial.println();

  //check topic of the message add new if you have more devices
  if (topic == "actuators/light") {
    Serial.print("Turnin of lights ");
    if (messageTemp == "1") {
      digitalWrite(relePin, HIGH);
      Serial.print("On");
    }
    else if (messageTemp == "0") {
      digitalWrite(relePin, LOW);
      prevState = 0;
      Serial.print("Off");
    }
  }
  Serial.println();
}


void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect("ESP8266Client")) {
      Serial.println("connected");
      //add new topics to subscribe if you have more devices
      client.subscribe("actuators/light");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

void setup() {
  pinMode(relePin, OUTPUT);
  pinMode(pirMotionPin, INPUT);
  Serial.begin(9600);
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  if (!client.loop())
    client.connect("ESP8266Client");
  sendSensorData();
  chekcPIR();
}

void sendData2(){
  int val = analogRead(A0);
    byte temp = 0;
    byte hum = 0;
    String output = "";
    int err = SimpleDHTErrSuccess;
    if ((err = dht11.read(dhtPin, &temp, &hum, NULL)) != SimpleDHTErrSuccess) {
      Serial.print("Read DHT11 failed, err="); Serial.println(err);
      return;
    }
    //outputing data about temperature and humidity
    output += "Temperature " + String((int)temp) + " Humidity " + String((int)hum);
    Serial.print("Publish message: ");
    strcpy(msg, output.c_str());
    Serial.println(msg);
    client.publish("sensorData/dht11", msg);

    //  get values of light sensors
    output = String(val);

    Serial.print("Publish message: ");
    strcpy(msg, output.c_str());
    Serial.println(msg);
    client.publish("sensorData/light", msg);
    strcpy(msg, output.c_str());
}
void sendSensorData() {
  long now = millis();
  if (now - lastMsg > dataTransimissionDelay) {
    lastMsg = now;
    sendData2();
  }
}


long timeFromLastMessagePIR = 0;
//5min
long timeForWhichPIRdataIsActual = 300000;
void chekcPIR() {
  byte state = digitalRead(pirMotionPin);
  if (state == 1 && prevState==0){
    sendData2();
    prevState = 1;
    timeFromLastMessagePIR = millis();
    strncpy(msg,"1",50);
    client.publish("sensorData/PIR",msg);
    Serial.println("sending data");
    //send mqtt message
    Serial.println("Somebody is in this area!");
  }else if(state==1 && prevState ==1){ // in case we just moved, so its still counts like we are in room.
    Serial.println("update time");   
    timeFromLastMessagePIR = millis();
  }
  else if (state == 0 && prevState == 1 && millis() - timeFromLastMessagePIR > timeForWhichPIRdataIsActual){
    Serial.print("sending not present data");
    timeFromLastMessagePIR = millis();
    prevState= 0;
    strncpy(msg,"0",50);
    client.publish("sensorData/PIR",msg);
    Serial.println("No one!");
  }
  delay(500);
}

