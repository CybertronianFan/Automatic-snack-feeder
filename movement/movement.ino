#include <ESP32Servo.h>

//Creating the servo objects
Servo panServo;
Servo tiltServo;

int panPin = 17; //Connect servo to pin IO17
int tiltPin = 18; //Connect servo to pin IO18

void setup()
{ 
  panServo.attach(panPin);  
  tiltServo.attach(tiltPin);

  //Initialises serial communication
  Serial.begin(115200);
}

void loop() {
}