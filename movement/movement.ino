#include <ESP32Servo.h>


//Declaring pan tilt, and the encoded message variable types
int pan;
int tilt;
String message;

//Creating the servo objects
Servo panServo;
Servo tiltServo;

int panPin = 17; //Connect servo to pin IO17
int tiltPin = 18; //Connect servo to pin IO18

void setup(){ 
  panServo.attach(panPin);  
  tiltServo.attach(tiltPin);

  //Initialises serial communication
  Serial.begin(115200);
}

void loop() {
  if (Serial.available() > 0){
    message = Serial.readStringUntil('\n');
    sscanf(message.c_str(), "%d,%d", &pan, &tilt);
    panServo.write(pan);
    tiltServo.write(tilt);
  }
}