#include <Servo.h>

int trigPin = 8; // TRIG pin
int echoPin = 9; // ECHO pin
int delayMs = 100;
int leftServoPin = 3;
int rightServoPin = 4;

Servo leftServo;
Servo rightServo;

void setup() {
  // put your setup code here, to run once:
  pinMode(trigPin, OUTPUT); // Configure trigger pin as output  
  pinMode(echoPin, INPUT); // Configure echo pin as input
  leftServo.attach(leftServoPin);
  rightServo.attach(rightServoPin);
  Serial.begin(9600);
}

void loop() {
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  float duration_us = pulseIn(echoPin, HIGH);
  float distance_cm = 0.017 * duration_us;

  // leftServo.write(0);
  // rightServo.write(0);
  // delay(1000);
  // leftServo.write(180);
  // rightServo.write(180);
  // delay(1000);

  Serial.println(distance_cm);

  if (Serial.available() > 0) {
    int s = Serial.read();
    leftServo.write(s);
    rightServo.write(s);
  }

  delay(delayMs);
}
