# RealSense

## Installation
**Ubuntu 20.04 is exploited here and strongly recommended**

1. [prerequisites](https://dev.intelrealsense.com/docs/compiling-librealsense-for-linux-ubuntu-guide#prerequisites) 
2. [Install Dependencies](https://dev.intelrealsense.com/docs/compiling-librealsense-for-linux-ubuntu-guide#install-dependencies)
3. [Install librealsense2](https://dev.intelrealsense.com/docs/compiling-librealsense-for-linux-ubuntu-guide#install-librealsense2)
4. [Build librealsense SDK](https://dev.intelrealsense.com/docs/compiling-librealsense-for-linux-ubuntu-guide#building-librealsense2-sdk)
5.  Launch librealsense SDK  
```
realsense-viewer   # run the command in terminal
```
## Firmware Update
1. [Download Firmware](https://dev.intelrealsense.com/docs/firmware-releases)
2. Update on SDK
* Launch SDK with command `realsense-viewer`
* Choose "More" -> "Update Firmware" and select the firmware downloaded before   
![Figure-1](/Figures/Figure-1.png "Figure-1")

## OpenCV(C++)
1. [Install OpenCV](https://github.com/IntelRealSense/librealsense/blob/master/wrappers/opencv/readme.md#linux)
2. Open Project
* Take rs-imshow as an example. Open "librealsense" -> "wrappers" -> "opencv" -> "imshow"
3. Edit CmakeLists and Run
* Add and change certain codes as below
```
find_package(OpenCV REQUIRED)

set(DEPENDENCIES realsense2 ${OpenCV_LIBS})

include_directories(${OpenCV_INCLUDE_DIRS})

target_link_libraries(rs-imshow ${DEPENDENCIES})
```
* Run the project in the terminal/vscode

## Yolov5 + Realsense + OpenCV(Python)
1. Use default Python3.8 in the system
2. Install certain packages
```
pip3 install pyrealsense2

pip3 install numpy

pip3 install python-opencv
```
3. [Install Pytorch](https://pytorch.org/features/)

4. Yolov5
* Clone codes from github repository
```
git clone https://github.com/ultralytics/yolov5.git
```
* Install required packages
```
pip3 install -r requirements.txt
```
5. Run Yolov5 + Realsense
* Put "realsense-detect.py" in Yolov5 project
* Run the project and get following result  
![Figure-2](/Figures/Realsense/Figure-2.png "Figure-2")

