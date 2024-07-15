#!/usr/bin/env python3
import numpy as np
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist

desired_steer = []
class Minimal_node(Node):
    def __init__(self):
        super().__init__('minimal_node')
        self.sub = self.create_subscription(Twist, 'cmd_vel', self.callback,10)

    def callback(self, msg):
            
        desired_feedback = msg.angular.z + 2
        self.get_logger().info(f'desired_feedback: {desired_feedback}')
        desired_steer.append(desired_feedback)
        self.get_logger().info(f'desired_steer: {desired_steer}')

def main(args=None):
    rclpy.init(args=args)
    minimal_node = Minimal_node()
    rclpy.spin(minimal_node)
    minimal_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

