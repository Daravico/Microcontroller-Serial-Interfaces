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

## Known issues.
The following are the problems that can be encountered when using this program:
- The AUTO mode has some glitches where other instructions are sent. This seems to be due to the timeout set for the Serial Communication. Could be adjusted but requires experimentation whether the messages are received or not. 
- The DoF are limited to 6. This can be changed but it is visually limited by the GUI. Small adjustments can be made for it.
- The GUI can be improved with better colors and a more friendly interface for the information that is being shown to the user.

## Possible improvements and future work.
Here is a list of the possible improvements that will take place in the future:
- **Inverse kinematics algorithm.** <br>
An algorithm that, depending on the actuators defined in the robotic configuration, can provide with an interaction with the robot such that the inverse kinematics are calculated. This requires a numerical approach, since the robot can be set with up to 6 DoF and the actuators can be either linear or rotatory types, meaning that there can be 64 combinations (2^6), making the geometrical solutions not viable. 

- **Guided programming.**<br>
It can be implemented a mode where the robot is manually placed by the user, saving the points of the configuration so that the robot can make paths according to those instructions received.

- **Velocity control.**<br>
An algorithm can be implemented so that the velocity of the placement for the received instructions can be set for smooth movement between signals. 

- **Digital Twin/Visual graph.**<br>
Either an option to visualize the robot on another interface or the full 3D representation with the possibility to be interacted with to become a full digital twin system.

## Resources used.
- Visual Studio Code ([Download](https://code.visualstudio.com/))

- Arduino IDE ([Download](https://www.arduino.cc/en/software))

- Python (3.10) + Libraries:
    - PySerial ([Documentation](https://pypi.org/project/pyserial/))
    - TTKBootstrap ([Documentation](https://ttkbootstrap.readthedocs.io/en/latest/))
    - NumPy ([Documentation](https://numpy.org/))

- 3D printed robot ([STL File Download](https://www.thingiverse.com/thing:3458238))


