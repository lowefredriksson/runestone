# Runestone

# Real-time-video

## Required software
This project requires the following software:
* opencv (https://opencv.org/)
* node (https://nodejs.org/en/)
* npm (https://www.npmjs.com/)

## Installation 

Run **npm install** at the root of the project to install the dependecies.

## Server  
To start the server run **node index.js**.

## Client 
To run the client, simply open the **index.html** file in a web browser. 

# Robot and Arduino
In order the get the EV3 robot to work with Python you first have to install EV3dev:
http://www.ev3dev.org/docs/getting-started/
After that you need the files robot.py and ar_signal.py in the robot from runestone/robot/. Arduino has to have uno-server.ino loaded and DHT22-sensor attached to the port described in the uno-server.ino from runestone/arduino/uno-server/. The arduino will be connected to the robot using USB. Once the Bluetooth communication between the robot and a computer is established you can run the robot.py from the robot which will wait for the connection from the client. From runestone/robot/ you can use client.py to act as temporary client for the robot if you put the MAC-address of the robot in the client.py.

