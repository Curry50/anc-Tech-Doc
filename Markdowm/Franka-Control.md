# Apply ROS on Franka

## Launch

1. Structure
```
├── CMakeLists.txt
├── config
│   ├── default_combined_controllers.yaml
│   ├── default_controllers.yaml
│   ├── franka_combined_control_node.yaml
│   ├── franka_control_node.yaml
│   └── start_pose.yaml
├── franka_controller_plugins.xml
├── include
│   └── franka_control
├── launch
│   ├── franka_combined_control.launch
│   ├── franka_control.launch
│   └── my_franka_control.launch
├── mainpage.dox
├── msg
│   └── info.msg
├── package.xml
├── rosdoc.yaml
├── scripts
│   └── talker.py
└── src
    ├── examples_common.cpp
    ├── franka_combined_control_node.cpp
    ├── franka_controller.cpp
    ├── franka_control_node.cpp
    ├── franka_state_controller.cpp
    └── torque_control.cpp
```
2. Overview
* All franka_ros packages are included here.
* franka_control is the aimed package that have been edited.
* Source Code is included in:  
(1) **talker.py**  
(2) **franka_controller.cpp**  
(3) **torque_control.cpp**    
* Further structure is demonstrated below  
(1) **talker.py -> vision node(Node 1)**  
(2) **franka_controller.cpp -> controller node(Node 2)**  
(3) **torque_control.cpp -> execution/state node(Node 3)**
![structure1](/Figures/Franka/structure1.png "structure1")

3. Instruction
* terminal 1  
```
roscore
```
* terminal 2  
```
cd ~/catkin_franka
catkin_make
source ./devel/setup.bash
rosrun franka_control talker.py
```
* terminal 3
```
cd ~/catkin_franka
catkin_make
source ./devel/setup.bash
roslaunch franka_control my_franka_control.launch robot_ip:=172.16.0.2
```

