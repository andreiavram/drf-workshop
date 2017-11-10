#include <MQTTClient.h>
#include <ESP8266WiFi.h>
#include <string.h>
#include <OneWire.h>
#include <SparkFunTSL2561.h>
#include <Wire.h>
#include <DallasTemperature.h>

/**

   Libraries:
   https://github.com/candale/esp_mqtt_arduino_wrapper
   https://github.com/sparkfun/TSL2561_Luminosity_Sensor_BOB/tree/master/Libraries/Arduino
   https://github.com/PaulStoffregen/OneWire
   https://github.com/milesburton/Arduino-Temperature-Control-Library
*/


extern "C" {
#include "user_interface.h"
}

#define ONE_WIRE_BUS 2  // DS18B20 pin

#define SENSOR 1
#define CALLABLE 2
#define ROLE SENSOR

const char* ssid = "SpyhceNew";
const char* pass = "Slayer!@#4";


os_timer_t statsTimer;
os_timer_t disableBuzz;
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature DS18B20(&oneWire);
SFE_TSL2561 light;
boolean gain;
unsigned int ms;


void log(const char* buf) {
  Serial.println(buf);
}

void log(String& buf) {
  Serial.println(buf);
}

class MyClient: public MQTTClient
{
    using MQTTClient::MQTTClient;

    void set(char* payload) {

    }

    void onData(String& topic, String& payload) {
      char topic_[100];
      char action[30];
      char* tok;
      Serial.print("Got topic: ");
      Serial.println(topic);

      Serial.print("Got payload: ");
      Serial.println(payload);

      strncpy(topic_, topic.c_str(), 100);
      tok = strtok(topic_, "/");
      tok = strtok(NULL, "/");
      tok = strtok(NULL, "/");

      if (strcmp(tok, "buzz") == 0) {
        log("Got buzz");
        int freq = atoi(payload.c_str());
        if (freq <= 0 || freq > 1023) {
          return;
        }
        analogWrite(D6, freq);
        os_timer_arm(&disableBuzz, 400, false);
      }
    }

    void onConnected() {
      log("Connected to MQTT broker");
      log("Subscribing to topics");
      subscribe("device/c/#", 1);
    }
};

MyClient* client;



void setupWifi() {
  log("Connecting to WiFI...");

  WiFi.begin(ssid, pass);
  while (WiFi.waitForConnectResult() != WL_CONNECTED) {
    Serial.print(".");
  }
  Serial.println("");

  WiFi.setAutoConnect(true);
  WiFi.setAutoReconnect(true);

  log("Connected to wifi");
}

void setupMqtt() {
  client = new MyClient("device", "212.47.229.77", "", "", 1884, 60);
  client->connect();
}

double getLum() {
  unsigned int data0, data1;

  if (light.getData(data0, data1))
  {
    double lux;    // Resulting lux value
    boolean good;  // True if neither sensor is saturated
    good = light.getLux(gain, ms, data0, data1, lux);

    return lux;
  }
  else
  {
    Serial.println("Error on getting light");
  }
}

void showStats(void* arg) {
  char strTemp[20];
  char strLum[20];

  DS18B20.requestTemperatures();
  float temp = DS18B20.getTempCByIndex(0);
  dtostrf(temp, 2, 2, strTemp);
  client->publish("device/temp", strTemp, strlen(strTemp), 1, 1);
  Serial.print("TEMP: ");
  Serial.println(temp);

  double lum = getLum();
  dtostrf(lum, 2, 2, strLum);
  client->publish("device/lum", strLum, strlen(strLum), 1, 1);
  Serial.print("LUX: ");
  Serial.println(strLum);
}


void unBuzz(void* arg) {
  analogWrite(D6, 0);
}


void user_init(void) {
  os_timer_setfn(&statsTimer, showStats, NULL);
  os_timer_setfn(&disableBuzz, unBuzz, NULL);
}

void setupLuminositySensor() {
  if (light.begin()) {
    log("Found sensor");
    unsigned char ID;
    gain = 1;
    light.setTiming(gain, 1, ms);
    light.setPowerUp();
  } else {
    log("No sensor?");
  }
}

void setup() {
  Serial.begin(115200);
  Serial.println();

  pinMode(D6, OUTPUT);
  analogWriteFreq(200);

  setupWifi();
  setupMqtt();
  setupLuminositySensor();

  user_init();
  os_timer_arm(&statsTimer, 1000, true);

}

void loop() {

}
