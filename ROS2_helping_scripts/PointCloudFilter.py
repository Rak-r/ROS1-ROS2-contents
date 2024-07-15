#!/use/bin/env python3
import pcl
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import PointCloud2, PointCloud
import numpy as np
import pdb
import sensor_msgs_py as sensor


class PointCloudFilter(Node):

    def __init__(self):
        super().__init__('pointcloud_filter')

        self.pointcloud_subscriber = self.create_subscription(PointCloud2, '/cloud_in', self.pointcloud_callback, 10)
        self.min_height = 0.0
        self.max_height = 0.0

    
    # def filter_points(self):
    #     pass
        # PointCloud2.
    
    def pointcloud_callback(self, msg):
        print(msg.data.shape)
        incoming_ranges = sensor.read_points(msg.data)
        #pdb.set_trace()

        # for range in incoming_ranges:
        #     print('incoming range', range)
        print(incoming_ranges)
    
def main(args=None):
    rclpy.init(args=args)

    pointcloud_filter = PointCloudFilter()
    try:
        rclpy.spin(pointcloud_filter)
    except:
        
        pointcloud_filter.destroy_node()
        rclpy.shutdown()
    
    

if __name__ == '__main__':
    main()

