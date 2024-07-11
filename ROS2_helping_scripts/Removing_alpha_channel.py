#!/usr/bin/env python3

'''

THis node handles the 4 channel problem which has been observed woth Zed camera and faces an incompatibility with object detection stack (YOLO).

THe script removes the alpha channel and re publihses the RGB image with corrected encoding

Change the topic name as per yours, DEFAULT --> STANDARD
'''

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2
import message_filters

class RemoveAlphaNode(Node):

    def __init__(self):
        super().__init__('remove_alpha_node')
        self.bridge = CvBridge()

        # Subscribers
        self.rgb_sub = message_filters.Subscriber(self, Image, "/zed/zed_node/rgb/image_rect_color")
        self.depth_sub = message_filters.Subscriber(self, Image, "/zed/zed_node/depth/depth_registered")

        # Synchronizer
        self.sync = message_filters.ApproximateTimeSynchronizer([self.rgb_sub, self.depth_sub], 10, 0.5)
        self.sync.registerCallback(self.camera_callback)

        # Publishers
        self.rgb_pub = self.create_publisher(Image, '/camera/color/image_raw', 10)
        self.depth_pub = self.create_publisher(Image, '/depth', 10)

    def camera_callback(self, rgb_msg, depth_msg):
        try:
            # Check if the encoding is 'bgra8' and convert it to 'bgr8'
            if rgb_msg.encoding == 'bgra8':
                cv_rgb_image = self.bridge.imgmsg_to_cv2(rgb_msg, desired_encoding='bgra8')
                cv_rgb_image = cv2.cvtColor(cv_rgb_image, cv2.COLOR_BGRA2BGR)
            else:
                cv_rgb_image = self.bridge.imgmsg_to_cv2(rgb_msg, desired_encoding='bgr8')

            # Convert depth image to OpenCV format
            cv_depth_image = self.bridge.imgmsg_to_cv2(depth_msg, desired_encoding='passthrough')

            # Convert back to ROS image messages
            rgb_msg_no_alpha = self.bridge.cv2_to_imgmsg(cv_rgb_image, encoding='bgr8')
            depth_msg_passthrough = self.bridge.cv2_to_imgmsg(cv_depth_image, encoding='passthrough')

            # Set the header
            rgb_msg_no_alpha.header = rgb_msg.header
            depth_msg_passthrough.header = depth_msg.header

            # Publish the processed images
            self.rgb_pub.publish(rgb_msg_no_alpha)
            self.depth_pub.publish(depth_msg_passthrough)

        except CvBridgeError as e:
            self.get_logger().error(f'CvBridge Error: {str(e)}')

def main(args=None):
    rclpy.init(args=args)
    node = RemoveAlphaNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
