#!/usr/bin/env


from time import sleep
from alpha1s import Alpha1S

robot = Alpha1S()

print("Battery status:")
print(robot.get_battery())

# Default position seems to be
# [90, 90, 90, 90, 90, 90, 90, 60, 80, 110, 90, 90, 120, 100, 90, 90]

while True:
    print(robot.servo_read_all())
    sleep(0.3)
