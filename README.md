# Robotic-Arm-Control-Using-Hand-Gestures
Use opencv to control the motion of robotic arm based on hand motion

Arduino here acts as servo ontrolling module as per the serial data sent through the connected serial port.The PWM mapping is
done in the code itself based the position of selected segment over resolution of each frame.Three motion of the robotic arm is possible(i.e. rotation about vertical axis, rotation about horizontal axis and the grip itself).Opencv is implemented here for image processing and the entire code runs in python.

I have automated thresholding procedure that makes the defination of threshold for the desired segment easier, you can directly select the segment to be trakced from the Tkinter window itself and it starts to function as per your hand movement(the segment should be attached to the hand whether a green tape or any desired color).

![alt text](https://github.com/abastola0/Robotic-Arm-Control-Using-Hand-Gestures/blob/master/robotic_arm.png)
