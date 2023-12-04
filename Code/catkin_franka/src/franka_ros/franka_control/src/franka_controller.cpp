#include <cmath>
#include <iostream>

#include "ros/ros.h"
#include "std_msgs/String.h"
#include "std_msgs/Float32MultiArray.h"
#include "std_msgs/Float32.h"
#include <franka/exception.h>
#include <franka/robot.h>
#include <vector>

// 定义全局变量，存储数据
double receive_x=0.0;
double receive_y = 0.0;
double state_receive = 0.0;
std::vector<float> angle_output={0,0};
char** argv1;

// 三维坐标的接收回调函数
void chatterCallback(const std_msgs::Float32MultiArray::ConstPtr& msg) 
{
        receive_x = msg->data[0];
        receive_y = msg->data[1];
        ROS_INFO_STREAM(receive_y);
}

// 机械臂状态的接收回调函数
void chatterCallbackState(const std_msgs::Float32::ConstPtr& msg)
{
    state_receive = msg->data;
    // ROS_INFO_STREAM("this is state receive");
    // ROS_INFO_STREAM(state_receive);
}

// 控制器的计算
void controller(double coord_x,double coord_y)
{
    double output_x = 100 * coord_x;  
    if(output_x >= 30.0f)
        output_x = 30.0f;
    else if(output_x <= -30.0f)
        output_x = -30.0f;
    double angle_x = M_PI/120 * output_x;

    double output_y = 100 * coord_y;  
    if(output_y >= 15.0f)
        output_y = 15.0f; 
    else if(output_y<= -5.0f)
        output_y = -5.0f;
    double angle_y = M_PI*(output_y/40-1/4);
    angle_output[0] = angle_x;
    angle_output[1] = angle_y;
}

int main(int argc, char** argv)
{
    // 节点初始化相关操作
    ros::init(argc, argv, "franka_controller_node");
    ros::NodeHandle nh;
    ros::Subscriber sub = nh.subscribe("chatter_vision", 1000, chatterCallback);
    ros::Subscriber sub_state = nh.subscribe("chatter_state",1000,chatterCallbackState);
    ros::Publisher pub = nh.advertise<std_msgs::Float32MultiArray>("chatter_control", 1000);
    ros::Rate loop_rate(1000);

    argv1 = argv;

    // 循环接收&发布力矩消息
    while(ros::ok())
    {
        std_msgs::Float32MultiArray msg;
        ros::spinOnce(); // 进入1次回调，接收Node1&Node3的反馈信息
        controller(receive_x,receive_y); // 控制器计算，此处的参数可自行修改
        ROS_INFO_STREAM("angle:x" << angle_output[0]);
        ROS_INFO_STREAM("angle:y" << angle_output[1]);
        msg.data = angle_output;
        pub.publish(msg); // 发布力矩消息
        loop_rate.sleep();
    }
}