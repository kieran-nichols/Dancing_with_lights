#!/usr/bin/env python
# Python file to read Xsens messages on ROS and send commands to change light

# Importing the libraries
import rospy
import time
from rospy.numpy_msg import numpy_msg
from std_msgs.msg import String, Float32MultiArray, MultiArrayDimension
import numpy

class LightNode():
   
    def __init__(self):
        rospy.init_node('light', anonymous=True)
        #Subscribbing to some topics
        print("init light node")
        rospy.Subscriber('xsens_com', Float32MultiArray, xsens_com_callback)
        rospy.Subscriber('xsens_joint_angle', Float32MultiArray, xsens_joint_angle_callback)
        
        # define callback functions for the ROS subscibers
        def xsens_com_callback(data):
            self.xsens_com = numpy.array(data.data)
    
        def xsens_joint_angle_callback(data):
            self.xsens_joint_angle = numpy.array(data.data)
        
        # Initialization and declaration of global-like (self) variables
        self.var1 = 0; self.var2 = 0
        self.prev_var1 = 0; self.prev_var2 = 0
        #self.xsens_com = numpy.array([0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=numpy.float32)
        #self.xsens_joint_angle = numpy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=numpy.float32)   

    # Connect to light
    def connect_light():
        # Veda put light connection code here
        pass

    # Send bluetooth cmds to light dependent on Xsens COM and joint angles
    def light_cmd():
        # Veda put light command code here
        pass

# main function
if __name__ == '__main__':
    try:
        LightNode().light_cmd()
        pass
    except rospy.ROSInterruptException: # ensures stopping if node is shut down
        pass

