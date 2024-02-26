#!/usr/bin/env python3
# 彩色帧率 = 深度帧率 = 58fps  
import rospy
import pyrealsense2 as rs
import numpy as np
import cv2
from time import sleep
from std_msgs.msg import Float32MultiArray
import math
import serial

# 串口初始化
# ser = serial.Serial('/dev/ttyUSB0',115200)

# Realsense初始化
pipeline = rs.pipeline()    # 定义流程pipeline，创建一个管道
config = rs.config()    # 定义配置config
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 60)      # 配置depth流
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 60)     # 配置color流
pipe_profile = pipeline.start(config)       # streaming流开始
align_to = rs.stream.color      # align_to 是计划对齐深度帧的流类型
align = rs.align(align_to)      # rs.align 执行深度帧与其他帧的对齐

intr_matrix = np.array([[606.852, 0, 326.237],  # 内参
                        [0, 606.744, 246.130], 
                        [0, 0, 1]],dtype = np.double)
dist_coeffs = np.zeros((5,1),dtype = np.double) # 畸变系数

# 节点初始化
rospy.init_node('talker',anonymous=True)

# 发布话题
def talker(data_send):
    pub_controller = rospy.Publisher('chatter_vision',Float32MultiArray,queue_size=10)
    rospy.loginfo(data_send)
    data_send = Float32MultiArray(data = data_send)
    pub_controller.publish(data_send)

 
# 获取对齐图像帧与相机参数
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

# 得到物体深度信息
def get_3d_camera_coordinate(depth_pixel, aligned_depth_frame, depth_intrin):
    x = depth_pixel[0]
    y = depth_pixel[1]
    dis = aligned_depth_frame.get_distance(x, y)        # 获取该像素点对应的深度
    camera_coordinate = rs.rs2_deproject_pixel_to_point(depth_intrin, depth_pixel, dis)
    return dis, camera_coordinate

# 计算相机坐标系原点到物体中心点的距离和偏角
def get_dis_angle(pixel_center):
    dis_center,coordinate_center = get_3d_camera_coordinate((int(pixel_center[0]),int(pixel_center[1])),aligned_depth_frame,depth_intrin)
    x_center,y_center,z_center = coordinate_center[0],coordinate_center[1],coordinate_center[2]
    distance = math.sqrt(x_center**2+z_center**2)*100
    alpha = math.atan2(x_center,z_center)*180/math.pi
    # print("x:" + str(int(x_center*100)) + " " + "y:" + str(int(y_center*100)) + " " + "z:" + str(int(z_center*100)))
    print(alpha)
    return distance,alpha

# 解算固定角pitch,yaw,roll
def GetEuler(rotation_vector):
    rot_matrix = cv2.Rodrigues(rotation_vector)[0]  # 旋转向量到旋转矩阵
    # 固定角的计算公式
    roll = 180/math.pi*math.atan2(rot_matrix[1][0],rot_matrix[0][0])       
    yaw = 180/math.pi*math.atan2(-rot_matrix[2][0],
                       math.sqrt(rot_matrix[0][0]*rot_matrix[0][0]+rot_matrix[1][0]*rot_matrix[1][0]))
    pitch = 180/math.pi*math.atan2(rot_matrix[2][1],rot_matrix[2][2])
    return pitch,yaw,roll

# 以选取点为原点，画出x,y,z三轴的投影
def draw(img, corners, imgpts):
    corner = list(corners[0].ravel())
    corner[0] = int(corner[0])
    corner[1] = int(corner[1])
    pts_store = [0,0,0]
    for i in range(0,3):
        pts_store[i] = [int(list(imgpts[i].ravel())[0]),int(list(imgpts[i].ravel())[1])]

    img = cv2.line(img, corner, pts_store[0], (255, 0, 0), 2)
    img = cv2.line(img, corner, pts_store[1], (0, 255, 0), 2)
    img = cv2.line(img, corner, pts_store[2], (0, 0, 255), 2)
    return img

# 识别红色矩形，提取角点
def red_detect(img):
    blue_ch,green_ch,red_ch = cv2.split(img)
    _,thresh = cv2.threshold(green_ch,100,255,cv2.THRESH_BINARY_INV)
    kernel = np.ones((3,3),np.uint8)
    thresh = cv2.GaussianBlur(thresh,(5,5),20,20)
    dilate = cv2.dilate(thresh,kernel)
    contours, _ = cv2.findContours(dilate, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for i in range(len(contours)):
        area_contour = cv2.contourArea(contours[i]) 
        rect = cv2.minAreaRect(contours[i]) # 最小外交矩形
        approx = cv2.approxPolyDP(contours[i], 0.01 * cv2.arcLength(contours[i], True), True) # 多边形逼近
        area_ratio = area_contour/(rect[1][0]*rect[1][1]) # 
        delta_y_01 = approx[1][0][1] - approx[0][0][1] # point 0&1的竖直距离
        delta_y_12 = approx[2][0][1] - approx[1][0][1] # point 1&2的竖直距离
        # 状态机筛选出目标矩形并判断矩形的倾斜情况
        if delta_y_01 < delta_y_12 and area_contour > 10000 and len(approx) == 4 and area_ratio > 0.8:  
            cv2.drawContours(img, [approx], 0, (255, 255, 0), 3) 
            pixel_left_up = approx[1][0]
            pixel_right_up = approx[0][0]
            pixel_right_down = approx[3][0]
            pixel_left_down = approx[2][0] 
            return pixel_left_up,pixel_right_up,pixel_right_down,pixel_left_down        
        elif delta_y_01 > delta_y_12 and area_contour > 10000 and len(approx) == 4 and area_ratio > 0.8:
            cv2.drawContours(img, [approx], 0, (255, 255, 0), 3)
            pixel_left_up = approx[0][0]
            pixel_right_up = approx[3][0]
            pixel_right_down = approx[2][0]
            pixel_left_down = approx[1][0]
            return pixel_left_up,pixel_right_up,pixel_right_down,pixel_left_down

if __name__=="__main__":
    while True:

        # 获取对齐图像帧与相机参数
        color_intrin, depth_intrin, img_color, img_depth, aligned_depth_frame,aligned_color_frame  = get_aligned_images() 

        try:
            pixel_left_up,pixel_right_up,pixel_right_down,pixel_left_down = red_detect(img_color)
            pixel_center = (pixel_left_up + pixel_right_down)/2
            cv2.circle(img_color, pixel_left_up, 8, [0,0,255], thickness=-1) # 左上 红色
            cv2.circle(img_color, pixel_right_up, 8, [0,255,0], thickness=-1) # 右上 绿色
            cv2.circle(img_color, pixel_right_down, 8, [255,0,0], thickness=-1) # 右下 蓝色
            cv2.circle(img_color, pixel_left_down, 8, [255,255,255], thickness=-1) # 左下 白色

            # 矩形的宽高，单位和焦距单位相同，均为mm
            width = 140 
            height = 240 

            obj_left_up = (-width/2,-height/2,0)
            obj_right_up = (width/2,-height/2,0)
            obj_right_down = (width/2,height/2,0)
            obj_left_down = (-width/2,height/2,0)

            # objpoints为角点的世界坐标，imgpoints为角点的像素坐标
            objpoints = np.array([obj_left_up,obj_right_up,obj_right_down,obj_left_down],dtype=np.double)
            imgpoints = np.array([pixel_left_up,pixel_right_up,pixel_right_down,pixel_left_down], dtype = np.double)
            
            ret,rotation_vector,translation_vector = cv2.solvePnP(objpoints,imgpoints,intr_matrix,dist_coeffs,flags=2)
            axis = np.float32([[100-width/2,-height/2,0], [-width/2,100-height/2,0], [-width/2,-height/2,100]]).reshape(-1,3)
            proj_imgpts, jac = cv2.projectPoints(axis, rotation_vector, translation_vector, intr_matrix, dist_coeffs)
            img_color = draw(img_color,imgpoints,proj_imgpts)
            pitch,yaw,roll = GetEuler(rotation_vector)
            # print("yaw:",int(yaw),"pitch:",int(pitch),"roll:",int(roll))

            distance,alpha = get_dis_angle(pixel_center)
            data_send_ros = (int(distance),int(alpha),int(yaw))
            # data_send_usart = (str(int(distance)).zfill(3) + str(int(alpha)).zfill(3) + str(int(yaw)).zfill(3) + "!")
            # ser.write(data_send_usart.encode())
            talker(data_send_ros)
        except:
            None
    
        # 显示画面
        cv2.imshow('RealSense',img_color)
        key = cv2.waitKey(1)
        if key & 0xFF == ord('q'): # 按q键停止
            break