#!/usr/bin/env


from alpha1s import Alpha1S
from time import sleep


# Connect to robot
print("Connecting... ", end="")
robot = Alpha1S()
print("Done")


# Read a single servo
servo = 0
while True:
    print(robot.servo_read(servo))
    sleep(0.3)


# Read all servo angles
while True:
    print(robot.servo_read_all())
    sleep(0.3)
