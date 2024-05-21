// Instructions are the following:
// Multiple (Example):
// M#Q0:0.450;Q1:1.520;Q2:-1.233;
// M#Q0:0;Q1:1.571;Q2:-1.571;
// Individual (Example):
// I#Q0:0.435;

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
int mapper(float x, float min_x, float max_x, float min_y, float max_y);

void setup() 
{
  // Serial initialization with baudrate specs.
  Serial.begin(9600); 
  Serial.setTimeout(50);

  // Servo pin attachments.
  servos[0].attach(9);
  servos[1].attach(10);
  servos[2].attach(11);
  
  int defaultValues[3];
  defaultValues[0] = map(0, rangesRadiansMin[0], rangesRadiansMax[0], rangesMicroSecondsMin[0], rangesMicroSecondsMax[0]);
  defaultValues[1] = map(PI/2, rangesRadiansMin[1], rangesRadiansMax[1], rangesMicroSecondsMin[1], rangesMicroSecondsMax[1]);
  defaultValues[2] = map(0, rangesRadiansMin[2], rangesRadiansMax[2], rangesMicroSecondsMin[2], rangesMicroSecondsMax[2]);

  // Default configuration.
  servos[0].writeMicroseconds(defaultValues[0]);
  servos[1].writeMicroseconds(defaultValues[1]);
  servos[2].writeMicroseconds(defaultValues[2]);
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
    int qIndex = instruction.substring(position + 1, position + 2).toInt();
    int startPos = instruction.indexOf(':', position) + 1;
    int finalPos = instruction.indexOf(';', position);

    // Extracting the ranges.
    int minMsRange = rangesMicroSecondsMin[qIndex];
    int maxMsRange = rangesMicroSecondsMax[qIndex];
    float minRadRange = rangesRadiansMin[qIndex]; 
    float maxRadRange = rangesRadiansMax[qIndex]; 

    // Saving the value.
    String individualValue = instruction.substring(startPos, finalPos);
    float radiansValue = individualValue.toFloat();
    
    // Mapping value to microseconds and sending.
    int value = mapper(radiansValue, minRadRange, maxRadRange, minMsRange, maxMsRange);
    servos[qIndex].writeMicroseconds(value);
    
    // Update to the index for the current position.
    position = finalPos + 1;
  }
}

/*********************************************************/

/* Individual instruction for one servo */
void individualCommand(String instruction)
{
  // Starting the index right after the double points.
  int startPos = instruction.indexOf(':') + 1;
  int finalPos = instruction.indexOf(';');

  // Getting the indexes of the instruction received.
  int qIndex = instruction.substring(3, 4).toInt();

  // Extracting the ranges.
  float minMsRange = rangesMicroSecondsMin[qIndex];
  float maxMsRange = rangesMicroSecondsMax[qIndex];
  float minRadRange = rangesRadiansMin[qIndex]; 
  float maxRadRange = rangesRadiansMax[qIndex]; 

  // Retreiving the value and making the conversion to degrees.
  String instructionValue = instruction.substring(startPos, finalPos);
  float radiansValue = instructionValue.toFloat();
    
  // Mapping value to microseconds and sending.
  int value = mapper(radiansValue, minRadRange, maxRadRange, minMsRange, maxMsRange);
  servos[qIndex].writeMicroseconds(value);
}

/* *********************************************** */
int mapper(float x, float min_x, float max_x, float min_y, float max_y)
{
  float m =  ( max_y - min_y ) / (max_x - min_x );
  float y = m * (x - min_x) + min_y;
  return (int)y;
}


