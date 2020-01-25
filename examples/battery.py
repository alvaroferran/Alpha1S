#!/usr/bin/env


from alpha1s import Alpha1S


# Connect to robot
print("Connecting... ", end="")
robot = Alpha1S()
print("Done")


# Read battery information
print("Battery status:")
print(robot.battery())
