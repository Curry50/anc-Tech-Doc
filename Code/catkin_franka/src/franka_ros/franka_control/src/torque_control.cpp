// Copyright (c) 2017 Franka Emika GmbH
// Use of this source code is governed by the Apache-2.0 license, see LICENSE
#include <cmath>
#include <iostream>

#include <franka/exception.h>
#include <franka/robot.h>
#include "ros/ros.h"
#include <franka_control/examples_common.h>
#include "std_msgs/String.h"
#include "std_msgs/Float32MultiArray.h"
#include "std_msgs/Float32.h"

/**
 * @example generate_joint_position_motion.cpp
 * An example showing how to generate a joint position motion.
 *
 * @warning Before executing this example, make sure there is enough space in front of the robot.
 */

// 定义全局变量，存储数据
double output_x = 0.0f;
double output_y = 0.0f;
double x=0.0f;
char** argv1;
double state_send = 0.0f;

// 读取机械臂状态，此处所需要的状态量可以修改
void ReadState(char** argv)
{
    franka::Robot robot(argv[1]);
    franka::RobotState robot_state = robot.readOnce();
    state_send = robot_state.O_T_EE[0];
}

// 接收力矩消息的接收回调函数,此处所需要的输出量可以修改
void chatterCallbackTorque(const std_msgs::Float32MultiArray::ConstPtr& msg) 
{
        output_x = msg->data[0];
        output_y = msg->data[1];
        ROS_INFO_STREAM(output_x);
}


int main(int argc, char** argv) {

    // 节点初始化&订阅&发布初始化
    ros::init(argc, argv, "franka_control_node");
    ros::NodeHandle nh;
    ros::Subscriber sub = nh.subscribe("chatter_control", 1000, chatterCallbackTorque);
    ros::Publisher pub = nh.advertise<std_msgs::Float32>("chatter_state",1000);
    ros::Rate r(1000);

    argv1 = argv;

  if (argc != 2) {
    std::cerr << "Usage: " << argv[0] << " <robot-hostname>" << std::endl;
    return -1;
  }
  try {
    franka::Robot robot(argv[1]);
    setDefaultBehavior(robot);

    // 移动机械臂到初始位置
    std::array<double, 7> q_goal = {{0, -M_PI_4, 0, -3 * M_PI_4, 0, M_PI_2, M_PI_4}};
    MotionGenerator motion_generator(0.6, q_goal);
    std::cout << "WARNING: This example will move the robot! "
              << "Please make sure to have the user stop button at hand!" << std::endl
              << "Press Enter to continue..." << std::endl;
    std::cin.ignore();
    robot.control(motion_generator);
    std::cout << "Finished moving to initial joint configuration." << std::endl;

    // 设置碰撞参数(待研究)
    robot.setCollisionBehavior(
        {{20.0, 20.0, 18.0, 18.0, 16.0, 14.0, 12.0}}, {{20.0, 20.0, 18.0, 18.0, 16.0, 14.0, 12.0}},
        {{20.0, 20.0, 18.0, 18.0, 16.0, 14.0, 12.0}}, {{20.0, 20.0, 18.0, 18.0, 16.0, 14.0, 12.0}},
        {{20.0, 20.0, 20.0, 25.0, 25.0, 25.0}}, {{20.0, 20.0, 20.0, 25.0, 25.0, 25.0}},
        {{20.0, 20.0, 20.0, 25.0, 25.0, 25.0}}, {{20.0, 20.0, 20.0, 25.0, 25.0, 25.0}});
  } catch (const franka::Exception& e) {
    std::cout << e.what() << std::endl;
    return -1;
  }
    // 工程主循环
    while (ros::ok()){
        std_msgs::Float32 state;
        state.data = state_send;
        ReadState(argv);//读取机械臂状态
        pub.publish(state);//发送机械臂状态
        ros::spinOnce(); //Node2->Node3 传递输出力矩/角度/速度
        franka::Robot robot(argv[1]);

    //     以下注释代码为力矩控制示例
    //     robot.control([&](const franka::RobotState&, franka::Duration) -> franka::Torques {
    //     return {{0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0}};
    //     });
        
        std::array<double, 7> q_goal = {{output_x, -M_PI_4, 0, -3 * M_PI_4-output_y, 0, M_PI_2, M_PI_4}};
        MotionGenerator motion_generator(0.6, q_goal);
        robot.control(motion_generator);
        r.sleep();
    }

  return 0;
}
