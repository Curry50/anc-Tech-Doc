#!/usr/bin/env python3
import rospy
import pyrealsense2 as rs
import numpy as np
import cv2
import socket, struct, os
from time import sleep
import matplotlib.pyplot as plt
from std_msgs.msg import Float32,Float32MultiArray
from std_msgs.msg import String
import torch
import torchvision.models as models

path = '/home/anc/yolov5/yolov5.pth'
model = torch.hub.load('/home/anc/yolov5', "custom",'./yolov5s.pt', source = 'local')

''' 
设置
'''
pipeline = rs.pipeline()    # 定义流程pipeline，创建一个管道
config = rs.config()    # 定义配置config
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 60)      # 配置depth流
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 60)     # 配置color流

pipe_profile = pipeline.start(config)       # streaming流开始

# 创建对齐对象与color流对齐
align_to = rs.stream.color      # align_to 是计划对齐深度帧的流类型
align = rs.align(align_to)      # rs.align 执行深度帧与其他帧的对齐

rospy.init_node('talker',anonymous=True)
kalman = cv2.KalmanFilter(2,2)
kalman.measurementMatrix = np.array([[1,0],[0,1]],np.float32)
kalman.transitionMatrix = np.array([[1,0],[0,1]],np.float32)
kalman.processNoiseCov = np.array([[1,0],[0,1]],np.float32) * 1e-3
kalman.measurementNoiseCov = np.array([[1,0],[0,1]], np.float32) * 0.01

def talker(coordiante):
    pub_controller = rospy.Publisher('chatter_vision',Float32MultiArray,queue_size=10)
    coord = (round(coordiante[0],3),round(coordiante[1],3))
    rospy.loginfo(coord)
    coord = Float32MultiArray(data = coord)
    pub_controller.publish(coord)
    # rate = rospy.Rate(10)
    # rate.sleep()


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

    return color_intrin, depth_intrin, img_color, img_depth, aligned_depth_frame,aligned_color_frame 


''' 
获取随机点三维坐标
'''
def get_3d_camera_coordinate(depth_pixel, aligned_depth_frame, depth_intrin):
    x = depth_pixel[0]
    y = depth_pixel[1]
    dis = aligned_depth_frame.get_distance(x, y)        # 获取该像素点对应的深度
    camera_coordinate = rs.rs2_deproject_pixel_to_point(depth_intrin, depth_pixel, dis)
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
            return x,y,w,h
        else:
            break

if __name__=="__main__":
    while True:
        ''' 
        获取对齐图像帧与相机参数
        '''
        color_intrin, depth_intrin, img_color, img_depth, aligned_depth_frame,aligned_color_frame  = get_aligned_images()        # 获取对齐图像与相机参数
        results = model(img_color)

        for result in results.xyxy[0]:
            x1, y1, x2, y2, confidence, class_id = result
            if int(class_id) == 39: #41 cup,47 apple,0 person,39 bottle
                x1,y1,x2,y2 = int(x1),int(y1),int(x2),int(y2)
                # center_pixel = (int((x1+x2)/2),int((y1+y2)/2)) 
                center_pixel = np.array([(x1+x2)/2,(y1+y2)/2],np.float32)
                mes = np.reshape(center_pixel[:],(2,1))
                center_pixel_cor = kalman.correct(mes)
                center_pixel_pre = kalman.predict()
                # center_pixel_pre = (int(center_pixel_pre[0]),int(center_pixel_pre[1]))
                # center_pixel = (int((x1+x2)/2),int((y1+y2)/2))  
                dis, camera_coordinate = get_3d_camera_coordinate(center_pixel, aligned_depth_frame, depth_intrin)
                camera_coordinate[0] = float(camera_coordinate[0])
                camera_coordinate[1] = float(camera_coordinate[1])
                camera_coordinate[2] = float(camera_coordinate[2])
                if camera_coordinate[0] != 0:
                    talker(camera_coordinate)
                center_pixel_pre = (int(center_pixel_pre[0]),int(center_pixel_pre[1]))
                # print(center_pixel_pre)
                center_pixel = (int((x1+x2)/2),int((y1+y2)/2))  
                ''' 
                显示图像与标注
                '''
                #### 在图中标记随机点及其坐标 ####
                cv2.circle(img_color, center_pixel, 8, [255,0,255], thickness=-1)
                cv2.circle(img_color, center_pixel_pre, 8, [255,0,0], thickness=-1)
                cv2.rectangle(img_color,(x1,y1),(x2,y2),(255,0,0),2)
                # color_fps = aligned_color_frame.get_frame_metadata(rs.frame_metadata_value.actual_fps)
                # 彩色帧率 = 深度帧率 = 58fps              
        #### 显示画面 ####
        cv2.imshow('RealSense',img_color)
        key = cv2.waitKey(1)
        if key & 0xFF == ord('q'):
            break