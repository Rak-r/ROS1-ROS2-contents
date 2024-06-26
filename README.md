# Using the Repository

1. Clone the repository. `git clone https://github.com/Rak-r/ROS1-ROS2-contents.git`

2. Navigate inside the repository directory. `cd <repo_directoy>`


3. Open termnal and type command:  `ros2 bag play odometry`

4. If want to visualise the topics, run:   `ros2 topic list -t`
 
5. If want to visualize properly in rviz2, then make sure nav2 is installed. https://navigation.ros.org/getting_started/index.html#installation
 
6. After installing NAV2, run: `rviz2 -d '/opt/ros/humble/share/nav2_bringup/rviz/nav2_default_rviz'`

7. You can also just run: `rviz2` in terminal.
   
#### Make sure to change the `global frame` to `map` to visualize the bag and add the topics `/odomerty/filtered`, `/map`, `/scan`.

### To see some plots, run the `rosbag_extarcter.py`.

### Before running the below script, if you want to vislaize all the message data fron `/odometry/filtered` topic from ros2 bag, try changing the `self.data_range` parameter to number of `/odometry/filtered` messages which can be visualised in the `metadata.yaml` of the ros2 bag.
* After specifying the range of messages, run in terminal: `python3 rosbag_extracter.py`


### The script can be expanded to visualise more data as required.








# ROS1-ROS2-contents
This repoistroy contains the information about the concepts of ROS1 and ROS2. It can also be suitable for porting the existing ROS1 projects to ROS2 as the repository mentions most of the possible erros and steps for new beginner to ROS/ROS2.

#### Major attention required: 
The launch files maybe of xml or python format but in ros2 there has been some changes in the name of arguements and attributes like `type>exec`, `ns>namespace`. Also the Navigation stack has been upgraded wuth some more functionalities and there has been chnages in the terms and packages. However the basic concept is the same as ROS1.

## PACKAGES WHICH HAS BEEN CHANGED ARE:

1. The Gmapping package for the mapping task in ROS1 with other skam packages like Karto, cartographer and the building `slam_toolbox` which steve mckenzie has introduced in ROS2, it basically offers structured functionality. Some parameters have been renamed but does the same task.

2. The Adaptive Monte Carlo Localization package of the nav_stack has te same adopted to nav2.

3. map_server apckage has been renamed to nav2_map_server: This package implements a server to handle the request of the map loading and also gives a map topic (map_server/map). There is also a map saver server running in the backend which saves the generated map according to the service requests.

4. nav2_plannar replaces the global planner in ROS2 and nav2_controller replaced the local planner.

### What is planner, controller, behaviour and smoother servers?
   #### Planners:
   * Planner serveer are used to compute the global plan or the shortest path.
   #### Controllers:
   * These servers are used to follow he the global plan generated by the planner. These were called a local planners in ROS1.
   #### Behaviors:
   * For instance, suppose the robot has been stuck at some point due to some obstackle coming in ts way. The behaviour servers makes it possible for the robit to act in thses king=d of scenarios through the actions like turning back, spinning which brings the robot into obstcakle free zone.
   #### Smoothers:
   * Sometimes we cannot fully rely on the path provided/computed by the plnner so we use the smoother server swhich helps in refining the planer path.
   #### Waypoint_Follower:
   * Navigation 2 features a nav2_waypoint_follower which has a plugin interface and helps to complete a specific task/operation for example; bringing the cup etc.

## STATE ETIMATION: THIS TASK IS DONE IN TWO STAGES:  

1. Firstly, to localise the robot a groundtruth odometry data is required which can be obtianed from various sensor s like wheel encoders, IMUs, GPS/GNSS, Visual Odometry, LiDAR based odometry approches also gaining a lot of popularity.
2. After getting the data, transformations required to make the robot's postion and orientation availale for Navigation and other applications, so `odom --> base_link` transform needs to be provided. Custom ROOS2  nodes can be created to publish the odometry message and the transforms.
3. Following the above, the senond task is to generate the map of the environment in which the robot is present. Various map libraries or `SLAM` algorithms are used to generate the map. ROS2 has provided support of `slam_toolbox`, an upgraded version of Karto package, whhich works good with 2d LiDAR data.
4. It subscribes to `LaserScan` messages and publishes the required `map>odom` frame transformation. This can be done with other methods as well namely; Cartographer, RTABMAP and ORB-SLAM (In case of RGB-D sesnors).

## Costmaps: 

Costmaps are the 2D occupancy grid maps which represents the environment for the robot. In these grids, the cell stores the value between (0-254) and the one with the value 0 means = No Occupancy while cell with value 254 = Lethally Occupied.
Costmaps have different layers which consist different information about the environment.

1. #### Static layer:
 * Represents the map section of the costmap.

3. #### Obstacle layer:
 * Represents the objects detected by the sensors that publishes either or both LaserScan and PointCloud messages.

5. #### Voxel layer:
 * Does the same thing as that of the obstacle layer but handles the 3D data.

7. #### Inflation layer:
 * Represents the added cost values around the obstacles.


### Joint state Publisher: 
In order to move the robot for a specific task or operation it is important to have the full detailed data of veery joint of the robot like the angle for the moving joint, displacemnet of linear actuator and velocity. Joint state publisher is used to keeping the track of this data and sends it to Robot state Publisher.

### Robot state Publisher: 
This recieves the data from the Joint state publisher and outputs the position and orientation of each coordinate frame and this data is pubishes to the TF2 library/package of ROS2 which keeps the track record for all the co-ordinate frames over time.

### TF2 library: 
It takes the input from the robot state publsher and is responsilble for keeping track of pose estimate and orientation of all coordinate frames over time.

### Fusion of sensors: 
The data recieved or collected from different sensors like LiDARs, Caneras, IMUs etc need to fused in order to use that infomation for robust working in different scenarios. To fuse the multi-sensor data, motion models are used and one of the most common method used is called Kalman Filtering. The Different-drive robot, Ackermann steered robot mostly uses Extended Kalman filtering (EKF) and partu=icle filter Monte Carlo method is used.

## 2D-LiDAR

If a robot is using 2d laser sensor then it has specific message type sensor_msgs/LaserScan which reprsents the data from the lidar sensor.
#### How?
*Each laserscan.msg contains a single sweep of the environment.
*Data is an array of floats representing range in metres.
*Tells which tf frame is the laser sensor is attached to.

## 3D-LiDAR

*When having a 3d lidar sensor on the robot, the data is best represented by pointclouds.
*Pointcloud is just a whole lot of points in the 3d space.
*ROS has specific message type for handling pointcloud data of 3d lidar through `sensor_msgs/PointCloud`.
*In case of sing RGB-D , stereo cameras for sensor input then, new message type has been provided by ROS community 'sensor_mssg/msg/PointCloud2`.


## SLAM ToolBox: (https://github.com/SteveMacenski/slam_toolbox)

ROS1 featured different SLAM approaches in order to build the map and perform localization. These methods are Gmapping, Cartograph, Karto Slam. In ROS2, the Gmapping has been replaced with Slam_toolbox.
Slam_toolbox works in the following way:

1. ROS Node: SLAM toolbox runs in synchronous mode and generates a ros node hwich subcribes tpo the laser scan and odometry topics and publishes map to odom transform and a map.

2. Getting LiDAR and Odometry Data: A callback from laser topic generates a pose and a laser scan is attached to the node. The posedscan objects makes a queue, which uis processed by the algorithm (Karto).

3. Pose Graph: The PosedScan object queue are used to form a pose graph which is utilised compute the robot pose and find loop closures.

4. Mapping: Laser scans associated to each pose in the Pose Graph are used to construct and publish a map.

5. Loop Closure: Ability of a SLAM algorithm to identify the previously detected images and correct the drift accumulated during the sensor movement.

The basic idea behind the Slam_toolbox or Gmapping in ROS1 is that we can create a map of the environment which can then be saved and used for navigation of the robot. 

### How to run the slam_toolbox in ROS2.

* Firstly, look at the congfiguartion file in the official `slam-toolbox` repository to get some idea of the terms. 
* Then just create the parameters/config in your robot workspace/src/robot_slam package. 
* Initially, copy the configs values for testing. Then create a launch file which can used from the reference from the repository only. 
* Build the package. <colcon build --symlink-install>
* `<source install/setup.bash>` (Don't forget to source the overlay i.e. `source /opt/ros/ros-distro/setp.bash`).
* Use the `<ros2 launch>` command to launch the slam_toolbox and view in rviz.
  
## Navigation 2(https://github.com/ros-planning/navigation2)

NAV2 Planners are used to compute the shortest path in the enviroment for the robot using the algorithms.

Different algorithms used:

1. #### NavFn:
 * This algorithm uses either Dijkstra or A*.
2. #### Smac 2D planner:
 * This implemnts a 2D A* algorithm using 4 or 8 connected neighbourhood with a smoother query.

#### Issue with these planners is that they may not be feasable to provide the map for the robot whch is Ackermann steered and legged robots.

3. #### SMAC Hybrid A* Planner:
 * This algorithm provides the support for Ackermann and legged robots and supports the Dubin and Reeds-Shepp motion nmodels.

#### Controller Server: 

Different Algorithms used:

1. DWB controller based on Dynamic window approach algorithm which have configurable plugins to compute the commands for the robots.

2.) Other controller server plugin is the TEB (Time Elastic Band) which optimizes the robot's trajectory based on its execution time, distance form obstacle and feasability w.r.t robot's kinematic constraints. Can be used fo Ackermann , legged robots.


### URDF/SDF

Coming to the structure for building the urdf file for the robot, xacro software can be used if the model is too complex. Things to keep in mind when dealing with URDF files.
Below are the list of common things to consider while developing the URDF. URDF files are used to describe the robot in the ros environment and SDF files are used to describe the robot in Gazebo simulation.

#### Link labels have three main tags:

1. Visual: Describes the robot visual properties (how it will look).
2. Collision: Physical properties that govern the robot collision with other objects.
3. Inertial: Describes some physics properties of the robot. (mass, inertia along axis, origin etc).

#### Joint tags/labels: 
* These are used to create the joint between two links. Includes name tag, type: Revolute for wheelss, continous etc, parent and child link names.

#### Errors in building URDF for robots:
1. Check the xml parsings and tags, correct spacing and tag closings.
2. In the urdf file define the base_footprint for ease and a joint fixing base-footprint with base_link/chassiss in case of car/4WD robots. carefully define the link lables with providing the origin tag, collision tag, visual tag.
3. Joint labels should be defined to show the connection between two links (parent and child).
4. Failed to find the root link: 2 root links found.

#### Solution: 
Set a parent link to one of those two links according to your robot structure.

5. Rviz2 not showing the mesh file and dae.file for your robot model.

#### Solution: 
* Make sure you added the meshes or the directory of your STL and .dae files to the CmakeLists.txt of the package which you are running.
* Secondly, try to use file://$(find package_name) instead of file://package in the mesh file path in your urdf.
* Thirdly, try to replace the path with the absolute path of the stl/dae files.

#### Note: Rviz2 axis colour and designation: x- Red, y-Green z-Blue. If Robot model appears in the rviz2 console and the joints are cluttered, then try to manipulate with the origin xyz and rpy values of those particular joints one by one and visualize the changes by launch file again and again.

6. To check the URDF is correctly built, try the command in the terminal : `check_urdf <name of the urdf file>`
### Gazebo integration issues

Gazebo converts the URDF to SDF format itself when passed through the launch files. Also, if using xacro, then it automatically parses the complete URDF to gazebo.(Later in this repo). There are lot of errors occur in Gazebo when using launch files to view the ROS URDF model in gazebo. 
I tried to mention the one I faced with some solutions below:
1. #### Warning: Non-unique names in gazebo simulation.
*Solution: Can ignore the warning or just use different names for each link and joint.
2. ####  Cannot have 2 joints with same name.
#### Meaning? 
A child link can have only one parent but a parent link can have as many child links. 
#### Solution:
Check in the urdf or sdf if a child link is having two/more parent link and correct it.

3. #### LoadJoint failed:
Correcting the above error will automatically resolve this one.
4. In ROS2, Joint State Publisher in gazebo plugin is used as `<joint_name> enter_the_name_of_the_joint</joint_name>`.
5. Gazebo server already in use: 
#### Solution: 
`killall gazebo` OR `killall gzserver` and restart terminal OR `sudo pkill -9 gzserver`. Use ps for more help.
  
After successfully building the urdf and viewing it in RViz and Gazebo, now to control the robot there are different ways.
* First method to move the robot in simulation is to use gazebo plugins which are already made available to users from gazebo. (Diff. drive, Tricycle Drive and others can be found at: https://github.com/ros-simulation/gazebo_ros_pkgs).
* Second method is newly introduced in ROS2, the ros2_control package. This involves a hardware interface,a controller manager and controller interface. The controller manager acts as a communication medium between the hardware interface and controller interface.
* Third, there are some diffrent robots with different kinematics models namely, Ackermann steered robot in our case and there is no support of gazebo plugin for this right now. There are some sources which uses ackermann steer robots, however these are based on ROS1. Therefore, to handle this issue we are struggling to find different ways to implement and acheive this. 
1. As per the design of the `OpenPodCar_1` consider a tracking rod connected to base link in the front to which the right and left pivots are connected and to the pivots the front right and front left wheels are connected.
2. Plan is to  apply force to the rod so that it can move in either right/left.

#### How done in OpenPodCar_1?

Ackermann demands the velocity message in x for logitudenal movemnet (front or reverse) and angular velocity in z (y) for steering angle movement.
So writing samll ros2 nodes can help with this. start with joystick package of ros2 and take the commands of the joystick node which outs the topic with message type /Joy.
Convert this /Joy message to speed command  (x) and angular command for wheel steer (z) using ros2 nodes joy2speed.py and joy2wheelangle.py.
After that, provide these converted messages to anothers nodes cmd_velhandler to get the main messages which are: joy2speed to /speedcmd_vel and joy2wheel to /wheelAnglecmd.

Then, a simple ros_gazebo plugin can be cretaed which will not do any calculations but just transfer the ros2 messages came form the small nodes to gazebo for simualtion and controlling. 
#### Gazebo Fortress/Garden and other new released versions supported

The new Gazebo Garden is used for the simulation of OpenPodCar_V2. The new gazebo features more functionalities with enhanced inetrface. As our robot behaves as car-like robot and features Ackermann-Steering kinematics. To maintain this behaviour in simulation the new gazebo now has an Ackermann system plugin which could be used according the robot configuartions. The plugin outputs standard Twist messages of field `linear.x` and `angular.z`. This also outputs the odometry information which might not be the correct odometry for the whole robot instead it is the odometry information for steering. To develop the communication between ROS2 and Gazebo the new package `ros_gz_bridge`  provides a message transportation bridge for most commonly used messages in ROS2.

#### Complete the installation of ros-gz bridge from source by selceting the Humble branch from the repo.(https://github.com/gazebosim/ros_gz/tree/humble)

#### Test it with:

1. one terminal: `gz sim`
2. second terminal: `gz topic -l` (lists all the available topics), then go to root of the workspace and source it using `source install/setup.bash`.

3. Initialize the bridge: `ros2 run ros_gz_bridge parameter_bridge <name of topic>@type of topic in ROS2[ignition.msgs.<type of topic in gazebo>`.

4. Third terminal: Try `ros2 topic pub` and see the bridge working.

#### Can also create Bi-directional bridge, GZ -->> ROS bridge as well.

Getting the odometry messages from the gazebo and sending it to ROS2 using `odometry_publisher gazebo plugin`.
Visualise the topic info and values in ros using 
`ros 2 topic echo <topic_name>`, `ros2 topic info <topic_name>`.

### Setting up NAV2 with  Gazebo

Install the NAV2 from the offcial documentation.

1. Points to look for: Sending the odom message to nav2 ?
2. Adding slam toolbox and look for parameters.

3. For nav2 we need the minimal transforms to be present

* `MAP -->> ODOM     AND     ODOM -->> BASE_LINK`

4. Map to odom transform is done by either AMCL if you are using pre built map and suitable for mostly inf=dor environment while if you want to build the map while moving the robot, then SLAM techniques are appointed which creates the map on the move and publishes `MAP to Odom` transform.
Then, launching the navigation file and set the initla pose using 2DPoseEstimate and once its set, hit the Navigate2GOAL button in rviz.

5. How the transform settled up for `odom to base_link` from gazebo.

7. Create the `GZ --> ROS` bridge for transferring the topic `/model/podcar/tf` which contains the transnform of `odom to base_link` to ROS2 side and remapp the topic to `/tf` as ROS publishes 2 simple topics related to transforms.
* /tf and /tf_static.

8. Check that the remapped tf topic getting the `odom to base_link` transform.

### NAV2 Errors

1. #### Map_server error [map-io]-->> Not able to load the map image, just check that correct path has been provided in the launc file argument.

2. #### [amcl-2] [ERROR] [1688743948.427156062] []:
*Original error: According to the loaded plugin descriptions the class differential with base class type nav2_amcl::MotionModel does not exist. Declared types are  nav2_amcl::DifferentialMotionModel nav2_amcl::OmniMotionModel

#### SOLUTION: 
*Change the parameter defination of robot_model_type : differential to nav2::DifferentialMotionModel

3. Transforms are not published (map-->odom) and (odom-->base_link).

4. Robot is jumping to and fro.
#### Reason -->> 
*It is because the when launching the AMCL and SLAM_TOOLBOX together both the nodes are publishing to the map topic and the transform (Map to Odom), which might interfare each other. To solve, try to disable AMCL from NAV2 CONFIG/PARAMS FILE.

5. Even after changing the NAV2 PARAMS under global and local costmap the parameter footprint-padding to double type, still showing the same issue 


6. #### [controller_server-1] terminate called after throwing an instance of 'rclcpp::exceptions::InvalidParameterTypeException'
   #### [controller_server-1]   what():  parameter 'footprint_padding' has invalid type: Wrong parameter type, parameter {footprint_padding} is of type {double}, setting it to {string} is not allowed.
 
7. Future error walkaround using this issue of github -->>
 * #### Changing the RWMs to Cyclone DDS. Link : https://github.com/ros-planning/navigation2/issues/3560 
  
 * Other error costmap might look:  https://github.com/ros-planning/navigation2/issues/2541
 
8. #### My issues for NAV2 :
 *Unable to run controller and planner server https://github.com/ros-planning/navigation2/issues/3703
 
 *Second Issue: Unable to use Smac planner based NAV2 params https://github.com/ros-planning/navigation2/issues/3717
 As suggest in issue number 8 above, just try to rebuild the workspace freshly to see the changes in NAV2 package. 
 

9. #### [controller_server-1] 2023-07-21 15:14:58.631 [RTPS_TRANSPORT_SHM Error] Failed init_port fastrtps_port7420: open_and_lock_file failed -> Function open_port_internal

   #### Similar issue: https://answers.ros.org/question/394404/rtps_transport_shm-error-and-at-the-same-time-no-topics-are-available-in-ros2-topic-list/
   
   #### SOLUTION (MAY TRY):
   * This error is due to different rmw_fastrtps versions. To check the versions in the ROS system use [SOLVED].
   * ros2 doctor --report | grep fastrtps

   #### To update the RMWs: `sudo apt update &&  sudo apt install ros-humble-rmw-fastrtps-cpp ros-humble-rmw-fastrtps-shared-cpp`

10. #### ERROR: bt navigator is not starting,
   #### Soltuion: 
   *try to provide he right Path to xml node in the nav2 params file or in the launch filea the default nav2 launch file suggests (DISAPPEARED).

11. Look for issue: https://github.com/ros-planning/navigation2/issues/3521

12. How to debug ROS2 code for getting the4 backtrace 
    * #### Debugger backtrace https://navigation.ros.org/tutorials/docs/get_backtrace.html 

13. NAV2 BT Navigator node not launching. 

#### ERROR: bt_navigator-4] [ERROR] [1690388832.138353661] []: Original error: Could not load library: libnav2_are_error_codes_active_condition_bt_node.so: cannot open shared object file: No such file or directory. [RESOLVED]

#### Solution:
*This might be because of some wrong configuration settings under the bt_navigator parameters in NAV2 params file.Check the parameters given are correct.
*Also, check which nodes are available for the specific ROS2 version. This might be the most probalble reason that the nodes passed in bt navigator parameter file is not availabel in the ros2 version installed. 

14. #### [INFO] [1691424608.497790289] [rviz]: Message Filter dropping message: frame 'odom' at time 3503.340 for reason 'the timestamp on the message is earlier than all the data in the transform cache'.
    #### [planner_server-2] [ERROR] [1691424804.953690738] [transformPoseInTargetFrame]: Extrapolation Error looking up target frame: Lookup would require extrapolation into the future.  Requested time 1691424773.212782 but the latest data is at time 3636.800000, when looking up transform from frame [map] to frame [odom]
    #### [planner_server-2] [WARN] [1691424804.953725100] [planner_server]: Could not transform the start or goal pose in the costmap frame
    #### [planner_server-2] [WARN] [1691424804.953756433] [planner_server]: [compute_path_to_pose] [ActionServer] Aborting handle.

15. #### [local_costmap.local_costmap]: Sensor origin at (0.34, 0.00 0.80) is out of map bounds (-1.45, -1.45, 0.00) to (1.52, 1.52, 0.78). The costmap cannot raytrace for it.

#### LINKS FOR SIMILAR ISSUES:

* LINK 1: https://answers.ros.org/question/384944/navigation-2-sensor-origin-out-of-map-bounds-the-costmap-cant-raytrace-for-it/
 
* LINK 2: https://answers.ros.org/question/415039/robot-and-sensor-are-out-of-map-bounds-local-costmap-voxel-layer/?answer=415074#post-id-415074

### HACKS

* #### (LINUX HACK) --->>> Use diff command from linux to check the difference between the files for easy visualization. (diff -y nav2_params.yaml navigation.yaml).
* #### ROS2 HACK ---> https://roboticsbackend.com/build-a-ros2-data-pipeline-with-ros2-topics/
* #### The last compatible version of `setuptools` wth ROS2 Humble is `58.2.0`.
   ** So to build python packages withput error do: `pip install setuptools==58.2.0 in usr or main system. not in venv`
 

#### See this issue --->>>>  https://robotics.stackexchange.com/questions/24036/lookup-would-require-extrapolation-into-the-future-on-the-same-machine

#### Might be related to time -->> https://answers.ros.org/question/379705/amcl-failed-to-transform-initial-pose-in-time/

### NAV2 ISSSUES WITH ROBOT CONTROL 

1. #### Check my github issue:
https://github.com/ros-planning/navigation2/issues/3737

2. #### LOOK THESE ISSUES AS WELL:
* https://github.com/ros-planning/navigation2/issues/2439
* https://github.com/ros-planning/navigation2/issues/3586
* https://github.com/ros-planning/navigation2/issues/3807
* https://robotics.stackexchange.com/questions/105003/nav2-robot-cant-create-valid-plan

#### Parameter to change for robot navigation in reverse:
*Just set the min_vel_x param in DWB controller to some negative value, say (-0.5) and try it.
(https://groups.google.com/g/ros-sig-navigation/c/z-9iCtvwGIA)

### Odometry for real OpenPodCar_V2

1. Looked for VO approaches but all of them a bit complicated and needs ros2 wrappers

2. Go with podcar's 1 laserscan matching style for getting the podcar 2' odometry.

### Laser Scan Matcher:
A laser scan matcher is an algorithm to estimate robot's motion or pose (position and orientation).
#### How?

*Firstly, the sensor maybe lidar or depth cameras which produces point clouds (can be converted to laserscan) and laser scans data is captured.
*Then, data aquisition takes place, meaning the lasersca data is represnetd in 2d space as a collect of 2d points consisting of objects in robot's surroundings.
*The scan matcher takes scans and tries to find the best relative transformation (translation and rotation) between them.
*Once, the best transformation is found it is used to compute the robot's odometry which includes chnages in (position and orientation)

#### Note: Laser scan matcher setteled up.

#### After lot of Hassle

The ROS2 navigation stack is working but some issues are still hanging.

#### STEPS:

1. Let the gazebo simulation run on its simulation time and publish the topics `/model/podcar/odometry`, `/lidar_scan` and the transform `odom to base_link` on `/tf` topic. 
2. The time stamp on these topics will be sim time of gazebo which starts from 0 seconds everytime the gazebo is launched.
3. After running gazebo, create small `ros2 nodes` which will convert the incoming messages from `gazebo time stamp ----->> unix time (wall time)`.
4. Once done, verify that the nodes are wroking and transferring messages correctly and make the topics names `/odom`, `/scan` to keep it simple for the NAV2. We can use whatever name we want using remapping.
5. After that, try launcho=ing the nav2 stack alomng with AMCL Localization and open rviz and view the terminal for some erros (if persists).
6. Then set the initial pose using 2dposeestimate in rviz2. Once done, hit the NAV2GOAL button nad see the robot moving in gazebo.


#### ROS2 Custom Messages

* To create custom message in ROS2, make the msg directory in the new package only for messages.
* Make sure that the name of the msg directory inside which all the messages are getting stored should only and only be "msg".
  
##### For the rest can follow the tutorial -->>  https://docs.ros.org/en/crystal/Tutorials/Custom-ROS2-Interfaces.html

### INTEL REALSENSE CAMERA INSTALLATION 
 
1. #### STEP 1
   Folow the guide for ros2 link for intel wraper -- (https://github.com/IntelRealSense/realsense-ros#installation-instructions)
   
     *Choose option 1 and click on linux debian installation guide and run commands mentioned line by line.

3. #### Now for specificaly ROS2 Integration 

*In the same repo:
*Under installation and step 2 : install latest Intel® RealSense™ SDK 2.0 

* select option 2:  Install librealsense2 package from ROS servers:  `sudo apt install ros-humble-librealsense2*`.

3. Then, install ROS2 Wrapper

*option 1 -->> `sudo apt install ros-humble-realsense2-*`

#### REALSENSE ROS2 wrapper to visualize pointclouds on Pointcloud2 message type

*`ros2 launch realsense2_camera rs_launch.py align_depth.enable:=true pointcloud.enable:=true`

#### REFER THIS: https://github.com/IntelRealSense/realsense-ros/issues/2295

### Making Teensy communicate with Ubuntu for serial connections   `https://www.pjrc.com/teensy/loader_linux.html`

#### Downloading serial in Linux/Ubuntu: `https://ubuntu.pkgs.org/22.04/ubuntu-main-amd64/python3-serial_3.5-1_all.deb.html'

* Grant permission to serial port for read and write in Linux using: `sudo chmod a+rw /dev/ttyACM0` replace the port name with whatever is it.

* Add user to dialout and tty group using: `sudo usermod -a -G tty <name_of_user>`,   `sudo usermod -a -G dialout <name_of_user>`


Add the udev rules to `/etc/udev/rules.d/

* How?

* Copy the udev rules from: `https://www.pjrc.com/teensy/00-teensy.rules` to a file create with name: `00-teensy.rules`

* Restart the terminal and serial code again and it should read the port.

#### Odometry estimation from steering input, ackermann robot, fusing VO and wheel odometry

* https://robotics.stackexchange.com/questions/110374/issues-while-setting-up-ekf-for-ackermann-steered-robot
* https://robotics.stackexchange.com/questions/105045/ukf-position-data-closely-match-slam-absolute-pose-regard-wheel-odometry/108335#108335

#### RTAB MAP related queries and setuo clues for ros2 with rgbd sensor intel realsense in my case.

* https://github.com/introlab/rtabmap_ros/issues/398
* http://wiki.ros.org/rtabmap_ros/Tutorials/SetupOnYourRobot
* https://github.com/introlab/rtabmap/issues/391
* https://github.com/introlab/rtabmap_ros/issues/467

#### Some links to estimate rotation angle for detected objects from cameras

* https://github.com/pauloabelha/Deep_Object_Pose/blob/master/src/dope.py

* https://github.com/IntelRealSense/librealsense/issues/7560

  


