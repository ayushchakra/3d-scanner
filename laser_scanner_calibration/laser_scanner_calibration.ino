#include <Servo.h>
Servo servo_pan;
Servo servo_tilt;
int sensor_pin = A0;
servo_pan_pin = 

void setup() {
  // put your setup code here, to run once:
  servo_pan.attach(9);
  servo_tilt.attach(11);
  pinMode(A0, INPUT);

  Serial.begin(9600);

  servo_pan.write(78);
  servo_tilt.write(41);
}

void loop() {
  // put your main code here, to run repeatedly:
  Serial.println(analogRead(sensor_pin));
  delay(50);
}
