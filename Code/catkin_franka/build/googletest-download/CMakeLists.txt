cmake_minimum_required(VERSION 3.0)
project(googletest-download VERSION "" LANGUAGES CXX)

include(ExternalProject)
ExternalProject_Add(googletest
  DOWNLOAD_NAME googletest-1.8.0.tar.gz
  URL https://github.com/google/googletest/archive/release-1.8.0.tar.gz
  URL_HASH SHA256=58a6f4277ca2bc8565222b3bbd58a177609e9c488e8a72649359ba51450db7d8
  SOURCE_DIR /home/anc/catkin_franka/src/franka_ros/libfranka/3rdparty/googletest
  BINARY_DIR /home/anc/catkin_franka/build/googletest
  DOWNLOAD_DIR /home/anc/catkin_franka/src/franka_ros/libfranka/3rdparty
  CONFIGURE_COMMAND ""
  BUILD_COMMAND ""
  INSTALL_COMMAND ""
  TEST_COMMAND ""
)
