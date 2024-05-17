// Instructions are the following:
// Multiple (Example):
// M#Q1:0.450;Q2:1.520;Q3:-1.233;
// Individual (Example):
// I#Q1:0.435;

#define PI 3.14159
#define COUNT_SERVOS 3

#include "Servo.h"

// Array to store the servos created.
Servo servos[COUNT_SERVOS];

// Array to hold the value of the instructions received.
float values_received[COUNT_SERVOS];

// Variable to receive the instructions via Serial Communication.
String instruction = "";

// Incoming Serial Data variable before conversion.
int incomingByte = 0; 

void setup() 
{
  // Serial initialization with baudrate specs.
  Serial.begin(115200); 
  Serial.setTimeout(50);

  // Servo pin attachments.
  servos[0].attach(9);
  servos[1].attach(10);
  servos[2].attach(11);
  
  // Default configuration.
  servos[0].write(180);
  servos[1].write(180);
  servos[2].write(180);
}

void loop() 
{
  if (Serial.available() > 0) {
    instruction = Serial.readStringUntil('\n');

    switch(instruction.charAt(0))
    {
      case 'I':
        Serial.println("Method 1");
        multipleCommands(instruction);
        break;
      case 'M':
        Serial.println("Method 2");
        break;
    }
  }
}

/* Multiple instructions for multiple servos */
void multipleCommands(String instruction)
{
  Serial.println(instruction);
}

/* Individual instruction for one servo */
void individualCommand(String instruction)
{
  Serial.println(instruction);
  Serial.println("Individual");

}

/* Mapper to translate radians to degrees */
float radiansToDegrees(float value)
{
  float result = value * 180 / PI;
  return result;
}
