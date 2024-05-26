# "Robot Serial Interface" for Learning Robotic Fundamentals.

## Index
- [Description of the project](#description-of-the-project)
- [Requirements](#requirements)
- [Explanation and usage](#explanation-and-usage)
- [Additional Notes](#additional-notes)
- [Known issues](#known-issues)
- [Possible improvements](#possible-improvements)
- [Resources used](#resources-used)

## Description of the project.
### What is this?
This project is aimed to be an aid in learning robotic fundamentals. It is possible to **visualize some important mathematical concepts used in robotics**, such as the transformation matrix, DH parameters to calculate the end effector's position, which is also displayed on screen. The information can be displayed in both radians and degrees as per the user convenience. 

### What this is not?
This is not nor it uses a standardized framework for robotics. It is neither recommended to be used at production. This project does not hide the mathematical parts to the end user, which is the main intention.
There is no PID or similar controller used (Although this can be seen as future improvements of the project), therefore the velocity and other important conditions are not taken in consideration, as well for the dynamics of the system. Only kinematic analysis is provided. 

### What to do with this project?
This can be used as a teaching tool, in order to observe the mathematical changes with certain parameters, both mathematically and physically. The system can also be used without a robot making certain configurations to the Serial Connection in order to have a better understanding on how the system makes the calculations.

## Requirements.
For this project, it is recommended to have the following components (The specific components used as an example will be described later):
- Physical components:
    - Robot with at least 1 Degree of Freedom (DoF).
    - Optional: Functional end effector.
    - Servomotors or related actuators.
- Electric components:
    - Any microcontroller.
    - DC Voltage Source (Common ones are from 5 to 24 V, but it is not limited to them).
    - Wires/jumpers.
- Software:
    - Python (3.10+). The following libraries were installed:
        - PySerial
        - TTKBootstrap
        - NumPy


## Explanation and usage.
### Workflow and diagrams.



Add here or add in each section. Include a general and specific ones.
INCLUDE VIDEO/GIF SAMPLES ON EACH EXPLANATION BELOW. 




### *Sample with 3 DoF*.
As an example on how to use this project, a demonstration is shown bellow using a robot with 3 DoF.

- The robot was 3D printed using black PLA. The link for the used model will be shared in the resources section. The model of the servomotors used were MG995, operating with a 5V voltage source.
![Robot Picture](/media/12-Robot%20iso.jpg) 
- The microcontroller board used to control the robot movement was an Arduino Uno (ATmega328P). This project can easily be adapted to other types of microcontroller, such as STM32 models or ESP32.
![Arduino micro Picture](/media/9-Arduino.jpg) 

#### Main Menu.
The principal menu consist of the different options that are available to be selected, being those the serial configuration to establish the settings for the connection with the robot, the robotic configuration, where details about the parameters are set and the direct kinematics option, where the robot is controlled why the user aid by some sliders that send instructions to the robot. **The two remaining options are not currently available**. 
Finally, there is the option to end the program, marked with a red button.

![Main Menu](/media/0-MainMenu.png)

#### Serial Configuration.

This frame is used to set the configuration to establish the connection with the robot. There is an option to load the available ports, showing both the name and the description for it. Another option gives the ability to set the baudrate specification, which also prevents the user to input characters other than digits.

![Serial Configuration](/media/0-SerialConfiguration.png)

#### Robotic Configuration.
![Robotic Configuration](/media/0-RoboticConfig.png)

#### Direct Kinematics Mode.
![Direct Kinematics Mode](/media/0-DKM.png)


## Additional notes.



## Known issues.




## Possible improvements.




## Future work.




## Resources used.



