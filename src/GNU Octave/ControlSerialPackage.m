% clear, clc

% Installing the Arduino Package.
% pkg install -forge arduino

% Loading the Package.
% pkg load arduino

% Opening the Arduino Setup Script.
% arduinosetup

% Creating the Arduino object.
% a = arduino('COM3');

% Visualizing the Arduino variables.
% a

% Turning on the LED as a demostration.
led_pin = "d13";

for i = 1:10
  writeDigitalPin(a, led_pin, 1);
  pause(0.5);
  writeDigitalPin(a, led_pin, 0);
  pause(0.5);
end

% Looking up for the available PWM terminals.
getPWMTerminals(a)

% Looking up for the available Servo terminals.
getServoTerminals(a)
