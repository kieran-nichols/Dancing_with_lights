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
import colour as Color
# ~ import seaborn as sns

            
class LightNode(): 
    def __init__(self):
        rospy.init_node('light', anonymous=True)
        
        #Subscribbing to some topics
        print("init light node")
        rospy.Subscriber('xsens_com', Float32MultiArray, self.xsens_com_callback)
        rospy.Subscriber('angular_moments', Float32MultiArray, self.xsens_angular_moments_callback)
        self.rate = rospy.Rate(10)
        # Initialization and declaration of global-like (self) variables
        self.x_pos = 0; self.y_pos = 0; self.z_pos = 0
        self.prev_brightness = 0
        self.prev_color = 0
        self.brightnesses = [x for x in range(1,100,1)]
        # ~ self.colors = cm.rainbow(numpy.linspace(0,1,10)) #[x for x in range(1,255,2)] #sns.color_palette("Spectral", 100).as_hex()
        #self.colors = [x for x in range(1,255,2)]
        self.red = Color.Color("red")
        self.colors = list(self.red.range_to(Color.Color("blue"),100))
        print(self.colors)
        
    def xsens_com_callback(self, data):
        self.xsens_com = numpy.array(data.data)
        self.x_pos = self.xsens_com[1]
        self.y_pos = self.xsens_com[2]
        self.z_pos = self.xsens_com[3]
        # print(self.x_pos,self.y_pos)
    
    def xsens_angular_moments_callback(self, data):
        self.xsens_angular_moment = numpy.array(data.data)
        self.pelvis_ang_vel = abs(self.xsens_angular_moment[4])
        # print(abs(self.xsens_angular_moment[4]))
              
    # Connect to light
    def connect_light(self):
        # try:
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

        # except:
        #     print("Can not connect")
    
     # Send bluetooth cmds to light dependent on Xsens COM and joint angles
    def light_cmd(self):
        
        self.connect_light()
        
        # Put light command code here
        while not rospy.is_shutdown(): # loop until node is shut down
            try:
                # ~ print("Command sent")
                x_max = 4
                x_min = -2.5
                y_min = -2.25
                y_max = 4.25
                z_min = 0.1
                z_max = 1.4
                spin_max = 200
                spin_min = 0
                
                # try:
                # Keep brightness between 0 and 100 for the min and max x distances of the room
                # brightness = self.brightnesses[int(max(0, min(100, (self.x_pos - x_min) / (x_max - x_min) * 100)))]

                # brightness = self.brightnesses[int(max(0, min(100, (self.z_pos - z_min) / (z_max - z_min) * 100)))]
                brightness = self.brightnesses[int(max(1, min(100, (self.pelvis_ang_vel - spin_min) / (spin_max - spin_min) * 100)))]

                # Keep color between 0 and 255 for the min and max y distances of the room
                color_var = max(1, min(100, (self.y_pos - y_min) / (y_max - y_min) * 100))
                # print(color_var)
                color = self.colors[int(color_var)]
                # print(color.rgb)
                color = [int(x*255) for x in color.rgb]
                # print(color)
                
                print(brightness, self.pelvis_ang_vel)

                #offset_x = 10
                #brightness = self.brightnesses[int(self.x_pos*10)+offset_x]
                #offset_y = 10
                #subset_x = (self.colors[int(self.x_pos*10)+offset_x])
                #subset_y = (self.colors[int(self.y_pos*10)+offset_y])
                #color = [subset_x,subset_y,0]
                        
                # set the color and brightness of the light
                self.my_device.setBrightness(brightness)
                self.my_device.setColor(color) # Sets entire light strip to new color

            except:
                brightness = self.prev_brightness
                color = self.prev_color
                print("An error occured")

            # remember previous light settings
            self.prev_brightness = brightness
            self.prev_color = color
            
            self.rate.sleep()

# main function
if __name__ == '__main__':
    try:
        LightNode().light_cmd()
        pass
    except rospy.ROSInterruptException: # ensures stopping if node is shut down
        pass

