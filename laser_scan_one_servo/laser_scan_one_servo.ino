#include <Servo.h>
// Declare servo object
Servo servo_tilt;

// Define infrared sensor and tilt servo pins
int infrared_sensor_pin = A0;
int servo_tilt_pin = 11;

// Define desired tilt angle sweep bound
int tilt_bound = 30;

// Define starting angle for tilt servo to make orientation flat
int tilt_start_angle = 41;

// Define the number of measurements to average at every position
int num_measurements = 5;

void setup() {
  // Initialize Digital PWM Pins for the pan and tilt servos
  servo_tilt.attach(servo_tilt_pin);
  
  // Initialize A0 to receive analog signals from infrared sensor
  pinMode(infrared_sensor_pin, INPUT);

  // Starts serial output to send to backend python 
  Serial.begin(9600);
}

void loop() {
  // Set tilt servo to default position (horizontal)
  servo_tilt.write(tilt_start_angle-tilt_bound);
  delay(1000);

  // For loop sweeps through tilt angles over entire tilt_bound and sends averaged scan results over serial
  for (int tilt_angle = tilt_start_angle-tilt_bound; tilt_angle < = tilt_start_angle+tilt_bound; tilt_angle++) {
    servo_tilt.write(tilt_angle)
    delay(50);
    // Once infrared sensor is in place, average 5 separate measurements
    // to determine the distance
    int sensor_value = 0;
    for (int i = 0; i < num_measurements; i++) {
      sensor_value += analogRead(sensor_pin);
      delay(50);
    }
    // Print the tilt angle and sensed distance over serial
    Serial.println(String(tilt_angle-tilt_start_angle) + " " + String(sensor_value/num_measurements));
    delay(50);
  }
  // Sends 'stop' message over serial to signal that current parameter sweep
  // iteration has completed
  Serial.println(28528);
}
