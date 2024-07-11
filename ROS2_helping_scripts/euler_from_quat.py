'''
simple python program to convert quaternian to yaw for 2D planar robots
'''


import math

def quaternion_to_yaw(x, y, z, w):
    # Ensure quaternion is normalized
    norm = math.sqrt(x**2 + y**2 + z**2 + w**2)
    x /= norm
    y /= norm
    z /= norm
    w /= norm

    # Calculate yaw angle
    yaw = math.atan2(2*(x*y + w*z), w*w + x*x - y*y - z*z)

    return yaw

# Given quaternion values
x = 0.0
y = 0.0
z = 0.14
w = 0.99

# Extract yaw angle
yaw = quaternion_to_yaw(x, y, z, w)

# Print yaw angle in radians
print("Yaw angle (radians):", yaw)

# Convert yaw angle to degrees
yaw_degrees = math.degrees(yaw)
print("Yaw angle (degrees):", yaw_degrees)
