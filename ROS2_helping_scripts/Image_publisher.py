#!usr/bin/env python3

'''
This node converts the any mp4 video file to corresponding ROS2 image messages.

Change the video path at line:23
'''

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2


class VideoPublisher(Node):
    def __init__(self):
        super().__init__('video_publisher')
        self.publisher = self.create_publisher(Image, '/camera/color/image_raw', 10)
        self.timer = self.create_timer(1.0 / 30, self.publish_frame)  # Assuming 30 FPS
        self.cv_bridge = CvBridge()
        self.cap = cv2.VideoCapture("/home/rakshit/Downloads/3_06_57_00.mp4")  # Specify the video path here

    def publish_frame(self):
        ret, frame = self.cap.read()
        if ret:
            ros_image = self.cv_bridge.cv2_to_imgmsg(frame, encoding='bgr8')
            self.publisher.publish(ros_image)

def main(args=None):
    rclpy.init(args=args)
    video_publisher = VideoPublisher()
    rclpy.spin(video_publisher)
    video_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
