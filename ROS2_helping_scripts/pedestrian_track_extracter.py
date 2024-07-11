#!/usr/bin/env python3

'''
The script can be used to extract and visualise the pedestrain track history in rviz2 using different Pedestrian track id.

Change the detection topic name with yours.

The script can be workied with standard ros2 vision message format wtih some message structure chnage if different.
'''

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Pose, Point
from visualization_msgs.msg import Marker, MarkerArray
from yolov8_msgs.msg import DetectionArray

class PedestrianTrajectoryVisualizer(Node):
    def __init__(self):
        super().__init__('pedestrian_trajectory_visualizer')
        self.subscription = self.create_subscription(
            DetectionArray, '/yolo/detections_3d', self.detection_callback, 10)
        self.publisher = self.create_publisher(MarkerArray, 'pedestrian_trajectories', 10)
        self.trajectories = {}

    def detection_callback(self, msg: DetectionArray):
        for detection in msg.detections:
            pose = detection.bbox3d.center
            
            if detection.id not in self.trajectories:
                self.trajectories[detection.id] = []
            
            self.trajectories[detection.id].append(pose)
        
        self.publish_trajectories(1.1, 1.0, 0.)

    def publish_trajectories(self, r, g ,b):
        marker_array = MarkerArray()

        for pedestrian_id, poses in self.trajectories.items():
            marker = Marker()
            marker.id = int(pedestrian_id)
            marker.type = Marker.LINE_STRIP
            marker.action = Marker.ADD
            marker.scale.x = 0.1
            marker.color.r = r
            marker.color.g = g
            marker.color.b = b
            marker.color.a = 1.0
            marker.header.frame_id = "map"

            for pose in poses:
                marker.points.append(Point(x=pose.position.x, y=pose.position.y, z=pose.position.z))
            
            marker_array.markers.append(marker)
        
        self.publisher.publish(marker_array)

def main(args=None):
    rclpy.init(args=args)
    node = PedestrianTrajectoryVisualizer()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
