#!/usr/bin/env python3
# 彩色帧率 = 深度帧率 = 58fps  
import rospy
import pyrealsense2 as rs
import numpy as np
import cv2
from time import sleep
from std_msgs.msg import Float32MultiArray
import torch

'''
初始化
'''
# Yolov5初始化
path = '/home/anc/yolov5/yolov5.pth'
model = torch.hub.load('/home/anc/yolov5', "custom",'./yolov5s.pt', source = 'local')

# Realsense初始化
pipeline = rs.pipeline()    # 定义流程pipeline，创建一个管道
config = rs.config()    # 定义配置config
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 60)      # 配置depth流
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 60)     # 配置color流
pipe_profile = pipeline.start(config)       # streaming流开始
align_to = rs.stream.color      # align_to 是计划对齐深度帧的流类型
align = rs.align(align_to)      # rs.align 执行深度帧与其他帧的对齐

# 节点初始化
rospy.init_node('talker',anonymous=True)

# 卡尔曼滤波初始化(Optional)
kalman = cv2.KalmanFilter(2,2)
kalman.measurementMatrix = np.array([[1,0],[0,1]],np.float32)
kalman.transitionMatrix = np.array([[1,0],[0,1]],np.float32) # 未设置状态转移矩阵
kalman.processNoiseCov = np.array([[1,0],[0,1]],np.float32) * 1e-3
kalman.measurementNoiseCov = np.array([[1,0],[0,1]], np.float32) * 0.01

# 发布话题
def talker(coordiante):
    pub_controller = rospy.Publisher('chatter_vision',Float32MultiArray,queue_size=10)
    coord = (round(coordiante[0],3),round(coordiante[1],3))
    rospy.loginfo(coord)
    coord = Float32MultiArray(data = coord)
    pub_controller.publish(coord)

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

if __name__=="__main__":
    while True:
        ''' 
        获取对齐图像帧与相机参数
        '''
        color_intrin, depth_intrin, img_color, img_depth, aligned_depth_frame,aligned_color_frame  = get_aligned_images()        # 获取对齐图像与相机参数
        results = model(img_color) # Yolov5模型推理

        ''' 
        主循环
        '''
        for result in results.xyxy[0]:
            x1, y1, x2, y2, confidence, class_id = result
            # COCO128数据及，具体label&id可上网查询
            if int(class_id) == 39:

                '''
                卡尔曼滤波(optional)
                center_pixel = np.array([(x1+x2)/2,(y1+y2)/2],np.float32)
                mes = np.reshape(center_pixel[:],(2,1))
                center_pixel_cor = kalman.correct(mes)
                center_pixel_pre = kalman.predict()
                center_pixel_pre = (int(center_pixel_pre[0]),int(center_pixel_pre[1]))
                '''

                # 数据类型转换
                x1,y1,x2,y2 = int(x1),int(y1),int(x2),int(y2)
                center_pixel = (int((x1+x2)/2),int((y1+y2)/2))  

                # 获取相机坐标系下的三维坐标
                dis, camera_coordinate = get_3d_camera_coordinate(center_pixel, aligned_depth_frame, depth_intrin)

                # 数据类型转换
                for i in range(0,3):
                    camera_coordinate[i] = float(camera_coordinate[i])

                if camera_coordinate[0] != 0:
                    talker(camera_coordinate)

                ''' 
                显示图像与标注
                '''
                
                # 画出中心点和矩形框
                cv2.circle(img_color, center_pixel, 8, [255,0,255], thickness=-1)
                cv2.rectangle(img_color,(x1,y1),(x2,y2),(255,0,0),2)  

        # 显示画面
        cv2.imshow('RealSense',img_color)
        key = cv2.waitKey(1)
        if key & 0xFF == ord('q'): # 按q键停止
            break