#include <Servo.h>

// Declare servo objects
Servo servo_pan;
Servo servo_tilt;

// Declare sensor pins for servo and infrared sensor
int infrared_sensor_pin = A0;
int servo_pan_pin = 9;
int servo_tilt_pin = 11;

// Define start angles for pan and tilt to make infrared
// sensor flat and horizontal
int pan_start_angle = 78;
int tilt_start_angle = 41;

void setup() {
  // Initialize servo pins
  servo_pan.attach(servo_pan_pin);
  servo_tilt.attach(servo_tilt_pin);

  // Initialize infrared pin for analog reading
  pinMode(infrared_sensor_pin, INPUT);

  // Initialize serial output to read sensor data
  Serial.begin(9600);

  // Write pan and tilt servos to flat and horizontal state
  servo_pan.write(pan_start_angle);
  servo_tilt.write(tilt_start_angle);
}

void loop() {
  // Constantly print the analog reading from the infrared sensor
  // to be analzyed and used to calculate calibration curve
  Serial.println(analogRead(sensor_pin));
  delay(50);
}
