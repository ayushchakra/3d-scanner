#include <Servo.h>
// Declare two servo objects
Servo servo_pan;
Servo servo_tilt;

// Define sensor and servo pins
int infrared_sensor_pin = A0;
int servo_pan_pin = 9;
int servo_tilt_pin = 11;

// Define the angle bounds for tilt and pan sweeps
int pan_bound = 15;
int tilt_bound = 10;

// Defines pan and tilt angles that orient infrared sensor horizontal and flat
int pan_start_angle = 78;
int tilt_start_angle = 41;

// Define the number of measurements at every position
int num_measurements = 5;

void setup() {
  // Initialize Digital PWM Pins for the pan and tilt servos
  servo_pan.attach(servo_pan_pin);
  servo_tilt.attach(servo_tilt_pin);
  
  // Initialize A0 to receive analog signals from infrared sensor
  pinMode(infrared_sensor_pin, INPUT);

  // Starts serial output to send to backend python 
  Serial.begin(9600);
}

void loop() {
  // Set pan and tilt servos to default position (flat and horizontal)
  servo_pan.write(pan_start_angle-pan_bound);
  servo_tilt.write(tilt_start_angle-tilt_bound);
  delay(1000);

  // Nested for loop that sweeps through the pan angles, increments tilt angle, reverses pan angles, and repeats
  // until the full pan_bound and tilt_bound have been scanned
  for (int tilt_angle = tilt_start_angle-tilt_bound; tilt_angle <= tilt_start_angle+tilt_bound; tilt_angle++) {
    servo_tilt.write(tilt_angle);
    delay(50);
    for (int pan_angle = pan_start_angle-pan_bound; pan_angle <= pan_start_angle + pan_bound; pan_angle++) {
      servo_pan.write(pan_angle);
      delay(50);
      // Once infrared sensor is in place, average 5 separate measurements
      // to determine the distance
      int sensor_value = 0;
      for(int i = 0; i < num_measurements; i++) {
        sensor_value += analogRead(sensor_pin);
        delay(50);
      }
      // Print the pan angle, tilt angle, and sensed distance over serial
      Serial.println(String(pan_angle-pan_start_angle) + " " + String(tilt_angle-tilt_start_angle) + " " + String(sensor_value/num_measurements));
      delay(50);
    }
    // Increment tilt angle
    tilt_angle++;
    servo_tilt.write(tilt_angle);
    delay(50);
    // Sweep through pan angles in reverse, following the same process as above
    for (int pan_angle = pan_start_angle+pan_bound; pan_angle >= pan_start_angle - pan_bound; pan_angle--){
      servo_pan.write(pan_angle);
      delay(50);
      // Once infrared sensor is in place, average 5 separate measurements
      // to determine the distance
      int sensor_value = 0;
      for(int i = 0; i < num_measurements; i++) {
        sensor_value += analogRead(sensor_pin);
        delay(50);
      }
      // Print the pan angle, tilt angle, and sensed distance over serial
      Serial.println(String(pan_angle-pan_start_angle) + " " + String(tilt_angle-tilt_start_angle) + " " + String(sensor_value/num_measurements));
      delay(50);
    }
  }
  // Sends 'stop' message over serial to signal that current parameter sweep
  // iteration has completed
  Serial.println(28528);
}
