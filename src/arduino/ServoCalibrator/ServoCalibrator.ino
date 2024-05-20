#include "Servo.h"

//Notes for calibration results.

/*
#define SQ1_MIN 750
#define SQ1_MAX 2275

#define SQ2_MIN 950
#define SQ2_MAX 1725

#define SQ3_MIN 1025
#define SQ3_MAX 1775
*/

Servo servo;

String instruction = "";

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600); 
  Serial.setTimeout(50);
  servo.attach(11);

}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available() > 0) 
  {
    instruction = Serial.readStringUntil('\n');

    Serial.println(instruction);
    servo.writeMicroseconds(instruction.toInt());

  }

}
