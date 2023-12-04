#!/usr/bin/env python3

import rospy
import pyrealsense2 as rs
import numpy as np
import cv2
import socket, struct, os
from time import sleep
import matplotlib.pyplot as plt
from std_msgs.msg import String
from std_msgs.msg import Float32

def talker(coordiante):
    pub = rospy.Publisher('chatter',Float32,queue_size=10)
    rospy.init_node('talker',anonymous=True)
    coord_float = coordiante[0]
    rospy.loginfo(coord_float)
    pub.publish(coord_float)


''' 
设置
'''
pipeline = rs.pipeline()    # 定义流程pipeline，创建一个管道
config = rs.config()    # 定义配置config
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 15)      # 配置depth流
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 15)     # 配置color流

# config.enable_stream(rs.stream.depth,  848, 480, rs.format.z16, 90)
# config.enable_stream(rs.stream.color, 848, 480, rs.format.bgr8, 30)

# config.enable_stream(rs.stream.depth,  1280, 720, rs.format.z16, 30)
# config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)

pipe_profile = pipeline.start(config)       # streaming流开始

# 创建对齐对象与color流对齐
align_to = rs.stream.color      # align_to 是计划对齐深度帧的流类型
align = rs.align(align_to)      # rs.align 执行深度帧与其他帧的对齐
 
def UDP_Send(coordinate):
    # -------------------------------- Initializing --------------------------------------------
    # Create a socket
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serveraddr = ("127.0.0.1", 9202)
    udp_socket.connect(serveraddr)
    count = 0
    # Create an increment for while loop
    send_msg_code = struct.pack("6d", float(coordinate[0]),float(coordinate[1]),1.3,1.4,1.5,1.6) #对应Simulin的六路数据接收
    udp_socket.sendto(send_msg_code, serveraddr)
    count += 1
    print(send_msg_code)
    sleep(0.01)
    # Close the udp socket.
    udp_socket.close()

''' 
获取对齐图像帧与相机参数
'''
def get_aligned_images():
    
    frames = pipeline.wait_for_frames()     # 等待获取图像帧，获取颜色和深度的框架集     
    aligned_frames = align.process(frames)      # 获取对齐帧，将深度框与颜色框对齐  

    aligned_depth_frame = aligned_frames.get_depth_frame()      # 获取对齐帧中的的depth帧 
    aligned_color_frame = aligned_frames.get_color_frame()      # 获取对齐帧中的的color帧

    #### 获取相机参数 ####
    depth_intrin = aligned_depth_frame.profile.as_video_stream_profile().intrinsics     # 获取深度参数（像素坐标系转相机坐标系会用到）
    color_intrin = aligned_color_frame.profile.as_video_stream_profile().intrinsics     # 获取相机内参


    #### 将images转为numpy arrays ####  
    img_color = np.asanyarray(aligned_color_frame.get_data())       # RGB图  
    img_depth = np.asanyarray(aligned_depth_frame.get_data())       # 深度图（默认16位）

    return color_intrin, depth_intrin, img_color, img_depth, aligned_depth_frame


''' 
获取随机点三维坐标
'''
def get_3d_camera_coordinate(depth_pixel, aligned_depth_frame, depth_intrin):
    x = depth_pixel[0]
    y = depth_pixel[1]
    dis = aligned_depth_frame.get_distance(x, y)        # 获取该像素点对应的深度
    # print ('depth: ',dis)       # 深度单位是m
    camera_coordinate = rs.rs2_deproject_pixel_to_point(depth_intrin, depth_pixel, dis)
    # print ('camera_coordinate: ',camera_coordinate)
    return dis, camera_coordinate

def orange_recognition(img_color):
    low_orange = np.array([0,43,46])
    high_orange = np.array([10,255,255])
    hsv_img = cv2.cvtColor(img_color,cv2.COLOR_BGR2HSV)
    k = np.ones((3,3),np.uint8)
    thresh = cv2.inRange(hsv_img,low_orange,high_orange)
    ero = cv2.erode(thresh,k)
    dila = cv2.dilate(ero,k)
    cv2.imshow("dila",dila)
    contours, _ = cv2.findContours(dila, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for i in range(len(contours)):
        x, y, w, h = cv2.boundingRect(contours[i])
        aspectRatio = float(w/h)
        areaRatio = cv2.contourArea(contours[i])/(w*h)
        if areaRatio > 0.8 and cv2.contourArea(contours[i]) > 1000 and 1.2 > aspectRatio > 0.8:
            break
    
    return x,y,w,h



if __name__=="__main__":
    while True:
        ''' 
        获取对齐图像帧与相机参数
        '''
        color_intrin, depth_intrin, img_color, img_depth, aligned_depth_frame = get_aligned_images()        # 获取对齐图像与相机参数

        try:
            x,y,w,h = orange_recognition(img_color)
        except:
            continue
        center_pixel = (int(x+w/2),int(y+h/2))
        dis, camera_coordinate = get_3d_camera_coordinate(center_pixel, aligned_depth_frame, depth_intrin)
        camera_coordinate[0] = float(camera_coordinate[0])
        camera_coordinate[1] = float(camera_coordinate[1])
        camera_coordinate[2] = float(camera_coordinate[2])
        ''' 
        获取随机点三维坐标
        '''
        # depth_pixel = [320, 240]        # 设置随机点，以相机中心点为例
        # dis, camera_coordinate = get_3d_camera_coordinate(depth_pixel, aligned_depth_frame, depth_intrin)
        # print ('depth: ',dis)       # 深度单位是mm
        # print ('camera_coordinate: ',camera_coordinate)

        ''' 
        显示图像与标注
        '''
        #### 在图中标记随机点及其坐标 ####
        cv2.circle(img_color, center_pixel, 8, [255,0,255], thickness=-1)
        # cv2.putText(img_color,"Dis:"+str(dis)+" m", (40,40), cv2.FONT_HERSHEY_SIMPLEX, 1.2,[0,0,255])
        cv2.rectangle(img_color,(x,y),(x+w,y+h),(255,0,0),2)
        cv2.putText(img_color,"X:"+str(camera_coordinate[0])+" m", (80,80), cv2.FONT_HERSHEY_SIMPLEX, 1.2,[255,0,0])
        cv2.putText(img_color,"Y:"+str(camera_coordinate[1])+" m", (80,120), cv2.FONT_HERSHEY_SIMPLEX, 1.2,[255,0,0])
        cv2.putText(img_color,"Z:"+str(camera_coordinate[2])+" m", (80,160), cv2.FONT_HERSHEY_SIMPLEX, 1.2,[255,0,0])
        
        #### 显示画面 ####
        cv2.imshow('RealSence',img_color)
        talker(camera_coordinate)
        # UDP_Send(camera_coordinate)
        key = cv2.waitKey(1)
        if key & 0xFF == ord('q'):
            break
