#include <Servo.h>

Servo myservo;
int sensorInPin = 2;
int sensorOutPin = 3;
int openPin = 5;
int closePin = 4;
bool doorOpen = false;

void setup() {
  pinMode(sensorInPin,INPUT);
  pinMode(sensorOutPin,OUTPUT);
  pinMode(openPin,INPUT);
  pinMode(closePin,INPUT);
  Serial.begin(9600);
  myservo.attach(10);
  myservo.write(0);
  delay(1000);
  myservo.write(90);
  delay(1000);
  myservo.write(    0);
 // attaches the servo on pin 10 to the servo object
}

void loop() {
 int isOpen = digitalRead(openPin);
 int closePinRead = digitalRead(closePin);
 digitalWrite(sensorOutPin,digitalRead(sensorInPin));
 if(isOpen == 1 && closePinRead == 0){
    if(!doorOpen){
      myservo.write(90);
      doorOpen = true;
     }
  }
  if(isOpen == 0 && closePinRead == 1){
    if(doorOpen){
      myservo.write(0);
      doorOpen = false;
     }
  }
}
