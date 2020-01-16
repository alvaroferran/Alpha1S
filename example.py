#!/usr/bin/env
from alpha1s import Alpha1S

robot = Alpha1S()

print("Battery status:")
print(robot.get_battery())
