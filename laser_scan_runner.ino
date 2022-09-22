#include <Servo.h>
Servo servo_pan;
Servo servo_tilt;
int pos = 0;
int pan_bound = 40;
int tilt_bound = 20;
int sensor_pin = A0;

void setup() {
  // put your setup code here, to run once:
  servo_pan.attach(9);
  servo_tilt.attach(10);
  pinMode(A0, INPUT);

  Serial.begin(9600);
  servo_pan.write(90-pan_bound);
  servo_tilt.write(90-tilt_bound);
  delay(1000);
  for (int tilt_angle = 90-tilt_bound; tilt_angle <= 90+tilt_bound; tilt_angle++) {
    servo_tilt.write(tilt_angle);
    delay(50);
    for (int pan_angle = 90-pan_bound; pan_angle <= 90 + pan_bound; pan_angle++) {
      servo_pan.write(pan_angle);
      Serial.println(String(pan_angle) + " " + String(tilt_angle) + " " + String(analogRead(sensor_pin)));
      delay(50);
    }
    tilt_angle++;
    servo_tilt.write(tilt_angle);
    delay(50);
    for (int pan_angle = 90+pan_bound; pan_angle >= 90 - pan_bound; pan_bound--){
      servo_pan.write(pan_angle);
      Serial.println("pan_angle: " + String(pan_angle) + " tilt_angle: " + String(tilt_angle)\
        + " sensor_output: " + String(analogRead(sensor_pin)));
      delay(50);
    }
  }
}

void loop() {
  // put your main code here, to run repeatedly:

  //  servo_1.write(0);
//  Serial.println(servo_1.read());
//  delay(2000);
//  servo_1.write(90);
//  Serial.println(servo_1.read());
//  delay(2000);
//  servo_1.write(180);
//  Serial.println(servo_1.read());
//  delay(2000);
//  pinMode(A0, INPUT);
}
