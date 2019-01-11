// uses: https://github.com/tyhenry/CheapStepper

// first, include the library :)

#include <CheapStepper.h>

/*
This device is supposed to receive a char '^' on the serial
when the motor has to spin clock wise and an '$' char when it
is supposed to spin counter-clockwise.

A second device (esp8266) sends this information over the serial bus
*/


CheapStepper stepper;
// here we declare our stepper using default pins:
// arduino pin <--> pins on ULN2003 board:
// 8 <--> IN1
// 9 <--> IN2
// 10 <--> IN3
// 11 <--> IN4

 // let's create a boolean variable to save the direction of our rotation

char dir = '$';

#define STEP_PIN 6
#define DIR_PIN 7


void setup() {

  // let's just set up a serial connection and test print to the console

  Serial.begin(115200);
  dir = '$';
}

void loop() {
  if(Serial.available() > 0) {
    char cmd = Serial.read();
    Serial.println(cmd);
    if(cmd == '^' && dir != '^') {
      dir = '^';
      for(int i = 0; i < 4; i ++) {
        for(int s = 0; s < 4096; s++) {
          stepper.step(true);
        }
      }
    } else if(cmd == '$' and dir != '$') {
      dir = '$';
      for(int i = 0; i < 4; i ++) {
        for(int s = 0; s < 4096; s++) {
          stepper.step(false);
        }
      }
    } else {

    }
  }
}

