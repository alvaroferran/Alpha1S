#!/usr/bin/env


from alpha1s import Alpha1S
from time import sleep


# Connect to robot
print("Connecting... ", end="")
robot = Alpha1S()
print("Done")


# Oscillate a single servo
while True:
    servo = 0
    for angle in range(0, 180, 10):
        robot.servo_write(servo, angle)
        sleep(0.3)
    for angle in range(180, 0, -10):
        robot.servo_write(servo, angle)
        sleep(0.3)


# Loop over different poses
init = [90, 90, 90, 90, 90, 90, 90, 60, 76, 110, 90, 90, 120, 104, 70, 90]
hands_up = [90, 180, 90, 90, 0, 90, 90, 60, 76, 110, 90, 90, 120, 104, 70, 90]
forward = [0, 0, 90, 180, 180, 90, 90, 60, 76, 110, 90, 90, 120, 104, 70, 90]
poses = [init, hands_up, forward]
while True:
    for pose in poses:
        robot.servo_write_all(pose)
        sleep(1)
