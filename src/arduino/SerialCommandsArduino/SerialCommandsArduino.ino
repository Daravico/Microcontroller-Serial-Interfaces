// Instructions are the following:
// Multiple (Example):
// M#Q1:0.450;Q2:1.520;Q3:-1.233;
// M#Q1:0;Q2:1.571;Q3:-1.571;
// Individual (Example):
// I#Q1:0.435;

#include "Servo.h"

// Constants used for calculation and storage.
#define PI 3.14159
#define COUNT_SERVOS 3

// -------------------------------
// Microseconds ranges.
#define SQ1_MIN 750
#define SQ1_MAX 2275

#define SQ2_MIN 950
#define SQ2_MAX 1725

#define SQ3_MIN 1025
#define SQ3_MAX 1775

// Radian ranges.
const float RQ1_MIN = - PI / 2;
const float RQ1_MAX = PI / 2;

const float RQ2_MIN = 0;
const float RQ2_MAX = PI / 2;

const float RQ3_MIN = 0;
const float RQ3_MAX = PI / 2;

// Arrays of values for the ranges.
float rangesRadiansMin[] = {RQ1_MIN, RQ2_MIN, RQ3_MIN};
float rangesRadiansMax[] = {RQ1_MAX, RQ2_MAX, RQ3_MAX};

int rangesMicroSecondsMin[] = {SQ1_MIN, SQ2_MIN, SQ3_MIN};
int rangesMicroSecondsMax[] = {SQ1_MAX, SQ2_MAX, SQ3_MAX};

// -------------------------------

// Array to store the servos created.
Servo servos[COUNT_SERVOS];

// Variable to receive the instructions via Serial Communication.
String instruction = "";

// Incoming Serial Data variable before conversion.
int incomingByte = 0; 

// Prototypes */
void multipleCommands(String instruction);
void individualCommand(String instruction);
int radiansToDegrees(float value);

void setup() 
{
  // Serial initialization with baudrate specs.
  Serial.begin(9600); 
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
  if (Serial.available() > 0) 
  {
    instruction = Serial.readStringUntil('\n');

    switch(instruction.charAt(0))
    {
      // Case of an individual command being received.
      case 'I':
        individualCommand(instruction);
        break;
      // Case of an multiple commands being received.
      case 'M':
        multipleCommands(instruction);
        break;
    }
  }
}

/*********************************************************/

/* Multiple instructions for multiple servos */
void multipleCommands(String instruction)
{
  int position = 2;

  for (int i = 0; i < COUNT_SERVOS; i++)
  {
    // Getting the indexes of the instruction received.
    int qIndex = instruction.substring(position + 1, position + 2).toInt() - 1;
    int startPos = instruction.indexOf(':', position) + 1;
    int finalPos = instruction.indexOf(';', position);

    // Saving the values.
    String individualValue = instruction.substring(startPos, finalPos);
    float radiansValue = individualValue.toFloat();
    
    // Transformation to degrees and sending.
    int degreesValue = radiansToDegrees(radiansValue);
    servos[qIndex].write(degreesValue);
    Serial.println(degreesValue);
    // int value = map(radiansValue, RQ1_MIN, RQ1_MAX, long, long)
    Serial.println();
    
    // Update to the index for the current position.
    position = finalPos + 1;
  }

/*
  while (position < instruction.length())
  {
    // Getting the indexes of the instruction received.
    int qIndex = instruction.substring(position + 1, position + 2).toInt() - 1;
    int startPos = instruction.indexOf(':', position) + 1;
    int finalPos = instruction.indexOf(';', position);

    // Saving the values.
    String individualValue = instruction.substring(startPos, finalPos);
    float radiansValue = individualValue.toFloat();

    // Transformation to degrees and sending.
    int degreesValue = radiansToDegrees(radiansValue);
    servos[qIndex].write(degreesValue);
    Serial.println(degreesValue);
    int value = map(radiansValue, RQ1_MIN, RQ1_MAX, long, long)
    Serial.println();
    
    // Update to the index for the current position.
    position = finalPos + 1;
  }*/
}

/*********************************************************/

/* Individual instruction for one servo */
void individualCommand(String instruction)
{
  // Starting the index right after the double points.
  int startPos = instruction.indexOf(':') + 1;
  int finalPos = instruction.indexOf(';');

  // Getting the indexes of the instruction received.
  int qIndex = instruction.substring(3, 4).toInt() - 1;

  // Retreiving the value and making the conversion to degrees.
  String instructionValue = instruction.substring(startPos, finalPos);
  float radiansValue = instructionValue.toFloat();
  int degreeValue = radiansToDegrees(radiansValue);
  Serial.println(degreeValue);

  // Sending the position to the servo.
  servos[qIndex].write(degreeValue);
}

/*********************************************************/

/* Mapper to translate radians to degrees */
int radiansToDegrees(float value)
{
  int result = value * 180 / PI;
  return result;
}
