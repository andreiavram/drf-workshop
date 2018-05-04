#include <MQTTClient.h>
#include <ESP8266WiFi.h>
#include <string.h>
#include <OneWire.h>
#include <SparkFunTSL2561.h>
#include <Wire.h>
#include <DallasTemperature.h>
#include <Adafruit_NeoPixel.h>

/**

   Libraries:
   https://github.com/candale/esp_mqtt_arduino_wrapper
   https://github.com/sparkfun/TSL2561_Luminosity_Sensor_BOB/tree/master/Libraries/Arduino
   https://github.com/PaulStoffregen/OneWire
   https://github.com/milesburton/Arduino-Temperature-Control-Library
   https://github.com/adafruit/Adafruit_NeoPixel
*/


extern "C" {
  #include "user_interface.h"
}

#define ONE_WIRE_BUS 2  // DS18B20 pin
#define NUMPIXELS 144

#define LED_BUZZ 1
#define TEMP_LUM_SERVO 2
#define ROLE LED_BUZZ

const char* ssid = "lasurub";
const char* pass = "Slayer!@#4";


os_timer_t statsTimer;
os_timer_t disableBuzz;

Adafruit_NeoPixel pixels = Adafruit_NeoPixel(NUMPIXELS, D7, NEO_GRB + NEO_KHZ800);
SFE_TSL2561 light;

OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature DS18B20(&oneWire);

boolean gain;
unsigned int ms;


void log(const char* buf) {
  Serial.println(buf);
}

void log(String& buf) {
  Serial.println(buf);
}


void all_pixels_to(int r, int b, int g) {
  for(int led_number = 0; led_number < NUMPIXELS; led_number++) {
     pixels.setPixelColor(led_number, pixels.Color(r, g, b));
  }
  pixels.show();
}

void pixels_range_to(int start, int end, int r, int b, int g) {
  if(start < 0) {
    log("bad start");
    return;
  }

  if(end > NUMPIXELS) {
    log("bad end");
    return;
  }

  for(int led_number = start; led_number <= end; led_number++) {
    pixels.setPixelColor(led_number, pixels.Color(r, g, b));
  }
  pixels.show();
}

class MyClient: public MQTTClient
{
    using MQTTClient::MQTTClient;

    void set(char* payload) {

    }

    void onData(String& topic, String& payload) {
      char topic_[100];
      char payload_[200];
      char action[30];
      char* tok;

      Serial.print("Got topic: ");
      Serial.println(topic);

      Serial.print("Got payload: ");
      Serial.println(payload);

      strncpy(topic_, topic.c_str(), 100);
      strncpy(payload_, payload.c_str(), 200);

      tok = strtok(topic_, "/");
      tok = strtok(NULL, "/");
      tok = strtok(NULL, "/");

      if (strcmp(tok, "buzz") == 0) {
        log("Got buzz");
        int freq, duration;

        tok = strtok(payload_, ",");
        freq = atoi(tok);
        tok = strtok(NULL, ",");
        duration = atoi(tok);

        if (freq <= 0 || freq > 1023) {
          log("bad freq");
          return;
        }

        if(duration < 0 || duration > 1000) {
          log("bad duration");
          return;
        }
        analogWrite(D6, freq);
        os_timer_arm(&disableBuzz, duration, false);
      }

      if(strcmp(tok, "led") == 0) {
        log("Got led");
        int led, r, g, b;
        bool is_range = false;
        char range[20];
        tok = strtok(payload_, ",");
        for(int i = 0; i < strlen(tok); i++) {
          if(tok[i] == '|') {
            is_range = true;
          }
        }
        if(is_range) {
          strcpy(range, tok);
        } else if(strcmp(tok, "all") == 0) {
          led = -1;
        } else if(strcmp(tok, "all_blink") == 0) {
          led = -2;
        } else {
          led = atoi(tok);
          if(led < 0 || led > NUMPIXELS) {
            log("bad led");
            return;
          }
        }

        tok = strtok(NULL, ",");
        r = atoi(tok);
        if(r < 0 || r > 255) {
          log("bad R");
          return;
        }

        tok = strtok(NULL, ",");
        g = atoi(tok);
        if(g < 0 || g > 255) {
          log("bad G");
          return;
        }

        tok = strtok(NULL, ",");
        b = atoi(tok);
        if(b < 0 || b > 255) {
          log("bad G");
          return;
        }

        if(is_range) {
          tok = strtok(range, "|");
          int start = atoi(tok);
          tok = strtok(NULL, "|");
          int end = atoi(tok);

          for(int i = 0; i < 3; i ++) {
            pixels_range_to(start, end, r, g, b);
            delayMicroseconds(350000);
            all_pixels_to(0, 0, 0);
            delayMicroseconds(200000);
          }
          
        } else if(led == -1) {
          all_pixels_to(r, g, b);
        } else if (led == -2) {
          for(int i = 0; i < 3; i ++) {
            all_pixels_to(r, g, b);
            delayMicroseconds(350000);
            all_pixels_to(0, 0, 0);
            delayMicroseconds(200000);
          }
        } else {
          pixels.setPixelColor(led, pixels.Color(r, g, b));
          pixels.show();
        }
        
        log("Writing to pixels");
      }

      if(strcmp(tok, "servo") == 0) {
        log("Got servo");
        int angle = atoi(payload_);
        if(angle < 0 || angle > 180) {
          log("bad angle");
          return;
        }

        // specific for the servos used
        int min_ = 85, max_ = 466;

        int pwmVal;
        if(angle == 0) {
          pwmVal = min_;
        } else {
          pwmVal = min_ + (max_ - min_) / 180 * angle;
        }

        Serial.print("Writing to servo: ");
        Serial.println(pwmVal);
        analogWrite(D5, pwmVal);
      }
    }

    void onConnected() {
      log("Connected to MQTT broker");
      log("Subscribing to topics");
      if(ROLE == LED_BUZZ) {
        subscribe("device/c/led", 1);
        subscribe("device/c/buzz", 1);
      } else if(ROLE == TEMP_LUM_SERVO) {
        subscribe("device/c/servo", 1);
      }

      log("Done MQTT init");
    }
};

MyClient* client;



void setupWifi() {
  log("Connecting to WiFI...");

  WiFi.begin(ssid, pass);
  while (WiFi.waitForConnectResult() != WL_CONNECTED) {
    Serial.print(".");
    delay(200);
  }
  Serial.println("");
  
  log("Connected to wifi");

  WiFi.setAutoConnect(true);
  WiFi.setAutoReconnect(true);

}

void setupMqtt() {
  if(ROLE == LED_BUZZ) {
    client = new MyClient("led_buzz", "212.47.229.77", "led_buzz", "coolpassword", 1884, 60);
  } else if(ROLE == TEMP_LUM_SERVO) {
    client = new MyClient("temp_lum_servo", "212.47.229.77", "", "", 1884, 60);
  }
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

void initAll() {
  setupWifi();
  setupMqtt();
  user_init();

  if(ROLE == LED_BUZZ) {
    pinMode(D6, OUTPUT);
    pixels.begin();
    log("Done led init");
  }

  if(ROLE == TEMP_LUM_SERVO) {
    analogWriteFreq(200);
    os_timer_arm(&statsTimer, 1000, true);
    setupLuminositySensor();
  }
  log("Done all init");
}

void setup() {
  Serial.begin(115200);
  Serial.println();

  initAll();
}

void loop() {

}


