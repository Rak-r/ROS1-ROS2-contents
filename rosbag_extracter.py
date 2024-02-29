
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from ackermann_msgs.msg import AckermannDrive
import matplotlib.pyplot as plt
import time
from geometry_msgs.msg import Twist
import numpy as np
class OdometryPublisher(Node):

    def __init__(self):
        super().__init__('odometry_publisher')

        self.odom_vx = []
        self.odom_vy = []
        self.ackermann_speed = []
        self.sub = self.create_subscription(Odometry, '/odometry/filtered', self.callback, 10)
        # self.twist_sub = self.create_subscription(Twist, '/cmd_vel', self.speed_callback, 10)
        self.ackermann_sub = self.create_subscription(AckermannDrive, '/ackermann_cmd', self.speed_callback, 10)
        self.get_logger().info('twist message extracter node is started')
        self.data_process = False
        self.data_range = 300

    def callback(self, msg):
        if len(self.odom_vx) < self.data_range and len(self.odom_vy) < self.data_range:
            self.odom_vx.append(msg.twist.twist.linear.x)
            self.odom_vy.append(msg.twist.twist.linear.y)
            print(f'VX : {msg.twist.twist.linear.x:.5f},  VY : {msg.twist.twist.linear.y:.5f}')
            print('\n')
            # print('odom lenght:', len(self.odom_speed))
            self.check_data_ready()

    def speed_callback(self, msg):
        speed = msg.speed
        if len(self.ackermann_speed) <self.data_range:
            self.ackermann_speed.append(speed)
            # print('ackermann length :', len(self.ackermann_speed))
            self.check_data_ready()

    def check_data_ready(self):
        if len(self.odom_vx) == self.data_range and len(self.odom_vy) == self.data_range:
            self.data_process = True

    def plot_data(self):
        if self.data_process:
            print('Plotting the data')
            
            plt.plot(self.odom_vx, label='Actual Speed vx')
            plt.plot(self.odom_vy, label='Actual Speed vy')
            # plt.xlabel('')
            plt.ylabel('Actual Speed')
            plt.title('Actual speed VX and VY')
            plt.legend()
            plt.show()
            # plt.savefig('Actual speed Vx and VY')
            time.sleep(1)

def main(args=None):
    rclpy.init(args=args)
    odometry_publisher = OdometryPublisher()
    while rclpy.ok() and not odometry_publisher.data_process:
        rclpy.spin_once(odometry_publisher)
    odometry_publisher.plot_data()
    odometry_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
