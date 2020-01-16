#!/usr/bin/env


from time import sleep
from alpha1s import Alpha1S

robot = Alpha1S()

# Read battery information
print("Battery status:")
print(robot.battery())

# # Read all servo angles
# while True:
#     print(robot.servo_read_all())
#     sleep(0.3)

# # Oscillate a single servo
# while True:
#     servo = 0
#     for angle in range(0, 180, 10):
#         print(robot.servo_write(servo, angle))
#         sleep(0.3)
#     for angle in range(180, 0, -10):
#         print(robot.servo_write(servo, angle))
#         sleep(0.3)

# Loop over different poses
init = [90, 90, 90, 90, 90, 90, 90, 60, 76, 110, 90, 90, 120, 104, 70, 90]
hands_up = [90, 180, 90, 90, 0, 90, 90, 60, 76, 110, 90, 90, 120, 104, 70, 90]
forward = [0, 0, 90, 180, 180, 90, 90, 60, 76, 110, 90, 90, 120, 104, 70, 90]
poses = [init, hands_up, forward]
while True:
    for pose in poses:
        robot.servo_write_all(pose)
        sleep(1)
