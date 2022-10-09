Our system is composed of a double-camera system: static and dynamic. The static camera which combines standard and depth information uses time-differential frames for motion recognition. The dynamic camera is on an closed-loop servo pan and tilt unit. The camera captures a zoomed-in frame of the ROI and feeds it to a DNN, which gives us the pixel coordinates of a drone within it. These coordinates are used for precise tracking of the drone.

Project demo in youtube:

[![Watch the video](https://img.youtube.com/vi/6wKWf0wkmmw/sddefault.jpg)](https://youtu.be/6wKWf0wkmmw)

Hardware:
- Nvidia Jetson Xavier AGX (board from connect tech)
- Intel® RealSense™ LiDAR Camera L515
- Servos from Phidget
- Camera zoom (120 fps)

The code is written in Python and YOLOv5 was used on Pytorch.

Students: Amir Sarig & Michael Aboulhair
Superviser: Andrey Zhitnikov

With the greate help of Eli Appleboim, Israel Berger, Yossi Bar Erez, Johanan Erez and Daniel Yagodin.
