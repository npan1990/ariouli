# Ariouli Robot

Ariouli is a software and hardware composition tailored to providing to our pets company when we are away from home.
It supports both autonomous and remote control versions.


https://github.com/npan1990/ariouli/assets/1937691/9fd6dd85-2844-4cd8-b958-eea16a62ca13



It supports:

1. Infrared Camera
2. Real-time control
3. Real-time Video
4. LiDAR Area Scanning
5. Servo Laser
6. MPU for localization

# Hardware Requirements

1. Raspberry Pi Zero 3 or newer
2. Two distinct power banks
3. MPU Sensor MPU-9250
4. Two Micro Servos
5. DC Motor Controller
6. Two or four DC Motors
7. Breadboard

# Software Installation

1. Install your favorite OS to the Raspberry
2. Clone this repository to the robot

# How to use

1. Login to the robot
2. Run a screen window
3. Inside the screen window run `./scripts/video.sh`
4. On your local computer open terminal and run 
`gst-launch-1.0 -v tcpclientsrc host=<ROBOTS IP> port=5000 ! gdpdepay ! rtph264depay ! avdec_h264 ! videoconvert ! autovideosink sync=false`
5. On the robot run `python ./src/simple.py` for simple usage.

# Controls

1. `Up`, `Down`, `Right`, `Left` arrows move the robot.
2. `Space` instantly stops the robot.
3. `L` enables the laser.
