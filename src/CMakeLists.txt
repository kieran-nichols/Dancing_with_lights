cmake_minimum_required(VERSION 2.8.3)
project(light_dance)

# for similar compile https://github.com/ros/ros_comm/blob/noetic-devel/clients/roscpp/CMakeLists.txt

## Compile as C++11, supported in ROS Kinetic and newer
#set(CMAKE_CXX_STANDARD 11)
#add_compile_options(-std=c++11)

## Find catkin macros and libraries
## if COMPONENTS list like find_package(catkin REQUIRED COMPONENTS xyz)
## is used, also find other catkin packages
find_package(catkin REQUIRED COMPONENTS
  rospy
  std_msgs
)

## System dependencies are found with CMake's conventions
# find_package(Boost REQUIRED COMPONENTS system)


## Uncomment this if the package has a setup.py. This macro ensures
## modules and global scripts declared therein get installed
## See http://ros.org/doc/api/catkin/html/user_guide/setup_dot_py.html
# catkin_python_setup()

################################################
## Declare ROS messages, services and actions ##
################################################

## To declare and build messages, services or actions from within this
## package, follow these steps:
## * Let MSG_DEP_SET be the set of packages whose message types you use in
##   your messages/services/actions (e.g. std_msgs, actionlib_msgs, ...).
## * In the file package.xml:
##   * add a build_depend tag for "message_generation"
##   * add a build_depend and a exec_depend tag for each package in MSG_DEP_SET
##   * If MSG_DEP_SET isn't empty the following dependency has been pulled in
##     but can be declared for certainty nonetheless:
##     * add a exec_depend tag for "message_runtime"
## * In this file (CMakeLists.txt):
##   * add "message_generation" and every package in MSG_DEP_SET to
##     find_package(catkin REQUIRED COMPONENTS ...)
##   * add "message_runtime" and every package in MSG_DEP_SET to
##     catkin_package(CATKIN_DEPENDS ...)
##   * uncomment the add_*_files sections below as needed
##     and list every .msg/.srv/.action file to be processed
##   * uncomment the generate_messages entry below
##   * add every package in MSG_DEP_SET to generate_messages(DEPENDENCIES ...)

## Generate messages in the 'msg' folder
# add_message_files(
#   FILES
#   Message1.msg
#   Message2.msg
# )

## Generate added messages and services with any dependencies listed here
# generate_messages(
#   DEPENDENCIES
#   std_msgs
# )

###################################
## catkin specific configuration ##
###################################
## The catkin_package macro generates cmake config files for your package
## Declare things to be passed to dependent projects
## INCLUDE_DIRS: uncomment this if your package contains header files
## LIBRARIES: libraries you create in this project that dependent projects also need
## CATKIN_DEPENDS: catkin_packages dependent projects also need
## DEPENDS: system dependencies of this project that dependent projects also need

catkin_package(CATKIN_DEPENDS rospy std_msgs)

###########
## Build ##
###########

#link_directories(lib/xspublic/xscontroller lib/xspublic/xscommon lib/xspublic/xstypes)
#link_directories(lib)

## Specify additional locations of header files
## Your package locations should be listed before other locations
include_directories(
  include
  #lib/xspublic
  #lib
  ${catkin_INCLUDE_DIRS}
)

set (SOURCES 
			ROS_light_command.py
			Light_display.py
)

#add_custom_target(xspublic
#  COMMAND +make -C ${CMAKE_CURRENT_SOURCE_DIR}/lib/xspublic
#)

## Declare a C++ executable
## With catkin_make all packages are built within a single CMake context
## The recommended prefix ensures that target names across packages don't collide
#add_executable(${PROJECT_NAME}_node ${SOURCES} ${HEADERS})



## Specify libraries to link a library or executable target against
#target_link_libraries(
#	${PROJECT_NAME}_node
#	PUBLIC 
#	xscontroller
#	xscommon
#	xstypes
#	pthread
#	dl
#	${catkin_LIBRARIES}
#)

#add_dependencies(roscpp ${${PROJECT_NAME}_EXPORTED_TARGETS} ${catkin_EXPORTED_TARGETS})




