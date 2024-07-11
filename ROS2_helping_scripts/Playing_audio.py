#!/usr/bin/env python3

'''
This is a fun ROS2 script to play with. This script plays an audio whenever a pedestrain is detected by the robot

'''

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image

from yolov8_msgs.msg import DetectionArray
from pygame import mixer

class AudioPlayerNode(Node):
    def __init__(self):
        super().__init__('audio_player')

        # self.sub = self.create_subscription(Image, '/depth', self.depth_cb, 10)
        self.pedestrian_pose_sub = self.create_subscription(DetectionArray, '/yolo/detections_3d', self.detections_cb, 10)  
        self.timer = self.create_timer(1.0, self.check_messages)
        self.messages_received = False
        self.mixer = mixer 
        self.mixer.init()
        self.song_loaded = False
        self.playing = False

    def detections_cb(self, msg): 
        self.messages_received = True
        if not self.song_loaded:
            # Load the song
            # TODO use spotify to play song or any smart modal to play the sound of some warning.

            self.mixer.music.load("/home/rakshit/Downloads/Rooster-Crow-A-www.fesliyanstudios.com.mp3") # specify the audio file.
            # Set the volume 
            self.mixer.music.set_volume(0.7) 
            self.song_loaded = True

        if msg:
            # Start playing the song if not already playing
         
            if not self.playing:
                self.mixer.music.play()
                self.playing = True

    def check_messages(self):
        if not self.messages_received and self.playing:
            print('No messages received. Pausing music...')
            self.mixer.music.stop()
            self.playing = False
        self.messages_received = False

def main(args=None):
    rclpy.init(args=args)
    audio_player_node = AudioPlayerNode()
    rclpy.spin(audio_player_node)
    audio_player_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
