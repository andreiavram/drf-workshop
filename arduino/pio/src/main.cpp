#include <ESP8266WiFi.h>
// #include <AccelStepper.h>
#include <MQTT.h>
#include <string.h>
#include <OneWire.h>
#include <Wire.h>
#include <Adafruit_NeoPixel.h>


#define ACTION_PIN D5
#define PRESS_TIME_MS 500

const char ssid[] = "internet";
const char pass[] = "mamaligacaacasa";
const char mqtt_client_id[] = "workshop";
const char mqtt_user[] = "workshop";
const char mqtt_pass[] = "VKlbYiIlutOsg5vjIKvbVA";

#define BUZZ_PIN D2
#define LED_PIN D7
#define NUMPIXELS 150
#define IN1 D1
#define IN2 D6
#define IN3 D5
#define IN4 D0

char motor_position;

// Include this to have access to lower level ESP8266 SDK
extern "C" {
  #include "user_interface.h"
}

os_timer_t disableBuzz;
os_timer_t period;

WiFiClient net;
MQTTClient client;
Adafruit_NeoPixel pixels = Adafruit_NeoPixel(NUMPIXELS, LED_PIN, NEO_GRB + NEO_KHZ800);
// AccelStepper stepper(4, IN1, IN2, IN3, IN4);

// OneWire oneWire(ONE_WIRE_BUS);
// DallasTemperature DS18B20(&oneWire);


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


void ping(void* arg) {
    Serial.println("Going at it");
    client.publish("device/k/pop", "");
}



void connect() {
    Serial.print("checking wifi...");
    while (WiFi.status() != WL_CONNECTED) {
        Serial.print(".");
        delay(1000);
    }

    Serial.print("\nconnecting...");
    while (!client.connect(mqtt_client_id)) {
        Serial.print(".");
        delay(1000);
    }

    Serial.println("\nconnected!");
    Serial.println("subscribing to topic");
    client.subscribe("device/c/led");
    client.subscribe("device/c/buzz");
    client.subscribe("device/c/motor");
    // os_timer_arm(&period, 1000, true);
}


void unBuzz(void* arg) {
  analogWrite(BUZZ_PIN, 0);
}


void messageReceived(String &topic, String &payload) {
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
        analogWrite(BUZZ_PIN, freq);
        os_timer_arm(&disableBuzz, duration, false);
    }

    if(strcmp(tok, "led") == 0) {
        // can send "<led_number>,<r_value>,<g_value>,<b_value>
        // can send "all,<r_value>,<g_value>,<b_value>"
        // can send "all_blink,<r_value>,<g_value>,<b_value>"
        // can send "3|10,<r_value>,<g_value>,<b_value>" to start a certain range of leds
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
            }
        } else if(led == -1) {
            log("settings all pixels");
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

    if(strcmp(tok, "motor") == 0) {
        Serial.println("Going for the motor");
        if(motor_position == '^') {
            Serial.println('$');
            motor_position = '$';
        } else {
            Serial.println('^');
            motor_position = '^';
        }
    }
}


void setup() {
    Serial.begin(115200);
    WiFi.begin(ssid, pass);
    pinMode(ACTION_PIN, OUTPUT);


    os_timer_setfn(&period, ping, NULL);
    os_timer_setfn(&disableBuzz, unBuzz, NULL);

    pixels.begin();

    motor_position = '$';

    client.begin("212.47.229.77", 1884, net);
    client.onMessage(messageReceived);

    connect();
}


void loop() {
    client.loop();
    // fixes some issues with WiFi stability
    delay(10);

    if (!client.connected()) {
        connect();
    }

}
