/*
String instruction = "";

int incomingByte = 0; // for incoming serial data

void setup() {
  Serial.begin(9600); // opens serial port, sets data rate to 9600 bps
}

void loop() {
  if (Serial.available() > 0) {
    instruction = Serial.readStringUntil('\n');

    if(instruction.charAt(0) == 'Q') 
    {
      int servoNumber = instruction.charAt(1) - '0';

      float angle = instruction.substring(3).toFloat();

      Serial.print("Servo: ");
      Serial.print(servoNumber);
      Serial.print(" Angle: ");
      Serial.println(angle);
    }
  }
}*/