#include <ESP32Servo.h>


//Declaring pan tilt, and the encoded message variable types
int pan;
int tilt;
String message;

//Creating the servo objects
Servo baseServo;
Servo upperArmServo;
Servo forearmServo;
Servo gripperServo;

int basePin = 16; //Connect servo to pin IO16
int upperArmPin = 17; //Connect servo to pin IO17
int forearmPin = 19; //Connect servo to pin IO19
int gripperPin = 18; //Connect servo to pin IO18

void setup(){ 
  baseServo.attach(basePin);  
  upperArmServo.attach(upperArmPin);
  forearmServo.attach(forearmPin);  
  gripperServo.attach(gripperPin);

  baseServo.write(90);
  upperArmServo.write(1556); //I installed it at 90 degrees and i find 75 to be optimal
  forearmServo.write(155);
  gripperServo.write(90);

  //Initialises serial communication
  Serial.begin(115200);
}

void loop() {
  if (Serial.available() > 0){
    message = Serial.readStringUntil('\n');
    sscanf(message.c_str(), "%d,%d", &pan, &tilt);
    baseServo.write(pan);
    forearmServo.write(tilt);

  }
}