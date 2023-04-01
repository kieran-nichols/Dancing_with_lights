#!/usr/bin/env python3
# Python file to read Xsens messages on ROS and send commands to change light

# Importing the libraries
import rospy
import time
from rospy.numpy_msg import numpy_msg
from std_msgs.msg import Float32MultiArray, MultiArrayDimension
import numpy
from govee_api_ble import GoveeDevice
from matplotlib import cm
# ~ import seaborn as sns

            
class LightNode(): 
    def __init__(self):
        rospy.init_node('light', anonymous=True)
        
        #Subscribbing to some topics
        print("init light node")
        rospy.Subscriber('xsens_com', Float32MultiArray, self.xsens_com_callback)
        rospy.Subscriber('xsens_joint_angle', Float32MultiArray, self.xsens_joint_angle_callback)
        self.rate = rospy.Rate(1)
        # Initialization and declaration of global-like (self) variables
        self.x_pos = 0; self.y_pos = 0
        self.prev_var1 = 0; self.prev_var2 = 0
        self.brightnesses = [x for x in range(1,100,1)]
        # ~ self.colors = cm.rainbow(numpy.linspace(0,1,10)) #[x for x in range(1,255,2)] #sns.color_palette("Spectral", 100).as_hex()
        self.colors = [x for x in range(1,255,2)]
        # ~ print(self.colors)
        
    def xsens_com_callback(self, data):
        self.xsens_com = numpy.array(data.data)
        self.x_pos = self.xsens_com[1]
        self.y_pos = self.xsens_com[2]
        print(self.x_pos,self.y_pos)
    
    def xsens_joint_angle_callback(self, data):
        self.xsens_joint_angle = numpy.array(data.data)
              
    # Connect to light
    def connect_light(self):
        # Put light connection code here
        print("Starting to connect")
        # Device setup
        self.my_device = GoveeDevice('A4:C1:38:59:43:27')#('A4:C1:38:59:43:27') D4:AD:FC:C1:2C:43
        # If I wait too long (more than 1 sec) then the bluetooth connection could fail
        #time.sleep(5) # need extra time to setup the connection

        # Ensure that the device starts as turned off
        self.my_device.setPower(False) # Turns device off
        time.sleep(0.1)

        # Turn on device
        self.my_device.setPower(True) # Turns device on
        self.my_device.setBrightness(1)
        time.sleep(1)
        print("Connected")
    
     # Send bluetooth cmds to light dependent on Xsens COM and joint angles
    def light_cmd(self):
        self.connect_light()
        # Put light command code here
        while not rospy.is_shutdown(): # loop until node is shut down
            # ~ print("Command sent")
            offset_x = 10
            brightness = self.brightnesses[int(self.x_pos*10)+offset_x]
            self.my_device.setBrightness(brightness)
            
            offset_y = 10
            subset_x = (self.colors[int(self.x_pos*10)+offset_x])
            subset_y = (self.colors[int(self.y_pos*10)+offset_y])
            color = [subset_x,subset_y,0]
            self.my_device.setColor(color) # Sets entire light strip to new color
            
            self.rate.sleep()

# main function
if __name__ == '__main__':
    try:
        LightNode().light_cmd()
        pass
    except rospy.ROSInterruptException: # ensures stopping if node is shut down
        pass

