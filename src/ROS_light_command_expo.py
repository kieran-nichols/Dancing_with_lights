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
from tada_ros.msg import IMUDataMsg
from tada_ros.msg import EuropaMsg

            
class LightNode(): 
    def __init__(self):
        rospy.init_node('light', anonymous=True)
        
        #Subscribbing to some topics
        print("init light node")
        rospy.Subscriber('europa_topic', EuropaMsg, self.handle_europa_input)
        rospy.Subscriber('sensing_topic', IMUDataMsg, self.handle_sensor_input)
        self.rate = rospy.Rate(10)
        # Initialization and declaration of global-like (self) variables
        self.fz = 0; self.mx = 0; self.my = 0
        self.gyro_x = 0
        self.gyro_y = 0
        self.gyro_z = 0
        self.gyro_norm = 0
        self.prev_brightness = 0
        self.prev_color = 0
        self.brightnesses = [x for x in range(1,100,1)]
        # ~ self.colors = cm.rainbow(numpy.linspace(0,1,10)) #[x for x in range(1,255,2)] #sns.color_palette("Spectral", 100).as_hex()
        #self.colors = [x for x in range(1,255,2)]
        self.blue = Color.Color("blue")
        self.red = Color.Color("red")
        self.colors = list(self.blue.range_to(self.red ,100))
        print(self.colors)
        
    def handle_sensor_input(self, data):
        # translates IMUDataMsg ROS message to IMUData class and stores
        # ~ try:
        self.gyro_x = data.gyro_x
        self.gyro_y = data.gyro_y
        self.gyro_z = data.gyro_z
        self.gyro_norm = abs(numpy.linalg.norm([self.gyro_x, self.gyro_y, self.gyro_z]))
        # ~ print(self.gyro_norm)
        # ~ except: 
            # ~ print("no data from IMU")

    def handle_europa_input(self, data):
        # translates IMUDataMsg ROS message to IMUData class and stores
        # ~ try:
        self.mx = data.mx
        self.my = data.my
        self.fz = data.fz
        # ~ print(self.mx, self.my, self.fz)
        # ~ except: 
            # ~ print("no data from Europa")
        
              
    # Connect to light
    def connect_light(self):
        # try:
        # Put light connection code here
        print("Starting to connect")
        # Device setup
        self.my_device = GoveeDevice('A4:C1:38:59:43:27')#('A4:C1:38:59:43:27') D4:AD:FC:C1:2C:43
        # If I wait too long (more than 1 sec) then the bluetooth connection could fail

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
                # mapping metrics for room and person
                y_min = 0
                y_max = 200
                spin_max = 300
                spin_min = 0
                
                # Keep brightness between 0 and 100 for the min and max distances or frontal pelvis ang vel of the room
                spin = self.gyro_norm
                if spin > spin_max: spin = spin_max
                brightness = self.brightnesses[int(max(0, min(100, (spin - spin_min) / (spin_max - spin_min) * 100)))]

                # Keep color between 0 and 255 for the min and max distances of the room
                y = abs(self.mx)
                if y > y_max: y = y_max
                color_var = max(0, min(100, (y - y_min) / (y_max - y_min) * 100))
                color = self.colors[int(color_var)]
                color = [int(x*255) for x in color.rgb]
                
                print(brightness, color_var)
                        
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

