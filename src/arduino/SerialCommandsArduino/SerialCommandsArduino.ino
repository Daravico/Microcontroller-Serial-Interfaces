#define LED 2
#include "BluetoothSerial.h"
BluetoothSerial SerialBT;

String instruction = "";

int incomingByte = 0; // for incoming serial data

void setup() {
  Serial.begin(9600); // opens serial port, sets data rate to 9600 bps
  digitalWrite(BUILTIN_LED, HIGH);
}

void loop() {
  if (Serial.available() > 0) {
    instruction = Serial.readStringUntil('\n');

    if(instruction.charAt(0) == 'Q') 
    {
      int servoNumber = instruction.charAt(1) - '0';

      float angle = instruction.substring(2).toFloat();

      Serial.print("Servo: ");
      Serial.print(servoNumber);
      Serial.print(" Angle: ");
      Serial.println(angle);
    }
  }
}