clear, clc
pause(2)

% -----------------------------------------------------------------
% ARDUINO SETUP.
% -----------------------------------------------------------------
%

% Installing the Arduino Package.
% pkg install -forge arduino

% Loading the Package.
% pkg load arduino

% Opening the Arduino Setup Script.
% arduinosetup

% Creating the Arduino object.
a = arduino('COM14');

% Visualizing the Arduino variables.
a

% Turning on and off the LED as a demostration.
led_pin = "d13";


for i = 1:10
  writeDigitalPin(a, led_pin, 1);
  pause(0.5);
  writeDigitalPin(a, led_pin, 0);
  pause(0.5);
end
