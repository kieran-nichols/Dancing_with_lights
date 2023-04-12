import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLabel
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import random
import rospy
import time
from rospy.numpy_msg import numpy_msg
from std_msgs.msg import Float32MultiArray, MultiArrayDimension
import numpy

## adapted from https://pythonspot.com/pyqt5-colors/

#class App(QMainWindow):

#    def __init__(self):
#        super().__init__()
#        self.title = 'PyQt rectangle colors - pythonspot.com'
#        self.left = 0
#        self.top = 0
#        self.width = 860
#        self.height = 1080
#        self.initUI()
        
#        rospy.init_node('light_window', anonymous=True)
        
#        #Subscribbing to some topics
#        print("init light_window node")
#        rospy.Subscriber('xsens_com', Float32MultiArray, self.xsens_com_callback)
#        rospy.Subscriber('angular_moments', Float32MultiArray, self.xsens_angular_moments_callback)
#        self.rate = rospy.Rate(1)
#        self.brightnesses = [x for x in range(1,100,1)]
        
#    def xsens_com_callback(self, data):
#        self.xsens_com = numpy.array(data.data)
#        self.x_pos = self.xsens_com[1]
#        self.y_pos = self.xsens_com[2]
#        self.z_pos = self.xsens_com[3]
#        #print(self.x_pos,self.y_pos)
    
#    def xsens_angular_moments_callback(self, data):
#        self.xsens_angular_moment = numpy.array(data.data)
#        self.pelvis_ang_vel = abs(self.xsens_angular_moment[4])
#        # print(abs(self.xsens_angular_moment[4]))
    
#    def initUI(self):
#        self.setWindowTitle(self.title)
#        self.setGeometry(self.left, self.top, self.width, self.height)
        
#        # Set window background color
#        self.setAutoFillBackground(True)
#        p = self.palette()
#        p.setColor(self.backgroundRole(), Qt.white)
#        self.setPalette(p)
#        #self.show()
        
#        # Add paint widget and paint
#        for i in range(10):
#            #while not rospy.is_shutdown(): # loop until node is shut down
#            self.m = PaintWidget(self)
#            self.m.move(0,0)
#            self.m.resize(self.width,self.height)
#            time.sleep(1)
#            self.show()
#            #self.rate.sleep()
    
        
#class PaintWidget(QWidget):
#    def paintEvent(self, event):
#        qp = QPainter(self)
        
#        qp.setPen(Qt.black)
#        size = self.size()
        
#        # mapping metrics for room and person
#        x_max = 4
#        x_min = -2.5
#        y_min = -2.25
#        y_max = 4.25
#        z_min = 0.1
#        z_max = 1.4
#        spin_max = 200
#        spin_min = 0
        
#        #while not rospy.is_shutdown(): # loop until node is shut down
#        # Keep brightness between 0 and 100 for the min and max distances or frontal pelvis ang vel of the room
#        brightness = self.brightnesses[int(max(1, min(100, (self.pelvis_ang_vel - spin_min) / (spin_max - spin_min) * 100)))]

#        # Keep color between 0 and 255 for the min and max distances of the room
#        color = max(1, min(100, (self.y_pos - y_min) / (y_max - y_min) * 100))
        
#        # Colored rectangles
#        #color = [200, 0, 0]
#        color_rgb = QColor(color[0], color[1], color[2])
#        color_hsv = color_rgb.getHsv()
#        print(color_rgb.getHsv(), color_hsv)
        
#        #brightness = 100
#        qp.setBrush(QColor.fromHsv(color_hsv[0], brightness, 255, 255))
#        qp.drawRect(0, 0, 1920, 1080)
        
#        #qp.move(0,0)
#        #qp.resize(self.width,self.height)
        
#        #self.show()
#            #self.rate.sleep()
        
#if __name__ == '__main__':
#    #app = QApplication(sys.argv)
#    #ex = App()
#    #sys.exit(app.exec_())
#    try:
#        app = QApplication(sys.argv)
#        ex = App().initUI()
#        #sys.exit(app.exec_())
#        pass
#    except rospy.ROSInterruptException: # ensures stopping if node is shut down
#        pass

import rospy
from std_msgs.msg import Int32
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtCore import QTimer

class MySubscriber:
    def __init__(self):
        self.integer_value = 0
        self.color = 0
        self.brightness = 0
        self.output = 0
        rospy.Subscriber('xsens_com', Float32MultiArray, self.xsens_com_callback)
        rospy.Subscriber('angular_moments', Float32MultiArray, self.xsens_angular_moments_callback)

    def xsens_com_callback(self, data):
        self.xsens_com = numpy.array(data.data)
        x_pos = self.xsens_com[1]
        y_pos = self.xsens_com[2]
        z_pos = self.xsens_com[3]
        y_min = -2.25
        y_max = 4.25
        self.color = max(1, min(100, (y_pos - y_min) / (y_max - y_min) * 100))
        #print(self.x_pos,self.y_pos)
    
    def xsens_angular_moments_callback(self, data):
        self.xsens_angular_moment = numpy.array(data.data)
        self.pelvis_ang_vel = abs(self.xsens_angular_moment[4])
        #print(abs(self.xsens_angular_moment[4]))
        spin_max = 600
        spin_min = 0
        self.brightnesses = [x for x in range(1,100,1)]
        self.brightness = self.brightnesses[int(max(1, min(100, (self.pelvis_ang_vel - spin_min) / (spin_max - spin_min) * 100)))]


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        color = my_subscriber.color
        brightness = my_subscriber.color
        self.output = str(color) + ',' + str(brightness)
        self.label = QLabel(self.output, self)
        self.setCentralWidget(self.label)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_label)
        self.timer.start(100)  # Update the label every 100ms

    def update_label(self):
        color = my_subscriber.color
        brightness = my_subscriber.color
        output = str(color) + ',' + str(brightness)
        self.label.setText(output)


if __name__ == "__main__":
    rospy.init_node("my_node")
    my_subscriber = MySubscriber()

    app = QApplication([])
    window = MyWindow()
    window.show()
    app.exec_()
    
#import rospy
#from std_msgs.msg import Int32
#from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
#from PyQt5.QtCore import QTimer

#class MySubscriber:
#    def __init__(self):
#        rospy.init_node('light_window', anonymous=True)
#        self.pelvis_ang_vel = 0
#        self.y_pos = 0
#        self.brightness = 0
#        self.color = [0,0,0]
#        #Subscribbing to some topics
#        print("init light_window node")
#        rospy.Subscriber('xsens_com', Float32MultiArray, self.xsens_com_callback)
#        rospy.Subscriber('angular_moments', Float32MultiArray, self.xsens_angular_moments_callback)
#        #self.rate = rospy.Rate(10)
#        #self.brightnesses = [x for x in range(1,100,1)]

#    def xsens_com_callback(self, data):
#        self.xsens_com = numpy.array(data.data)
#        x_pos = self.xsens_com[1]
#        y_pos = self.xsens_com[2]
#        z_pos = self.xsens_com[3]
#        y_min = -2.25
#        y_max = 4.25
#        self.color = max(1, min(100, (y_pos - y_min) / (y_max - y_min) * 100))
#        #print(self.x_pos,self.y_pos)
    
#    def xsens_angular_moments_callback(self, data):
#        self.xsens_angular_moment = numpy.array(data.data)
#        self.pelvis_ang_vel = abs(self.xsens_angular_moment[4])
#        # print(abs(self.xsens_angular_moment[4]))
#        spin_max = 200
#        spin_min = 0
#        self.brightnesses = [x for x in range(1,100,1)]
#        self.brightness = self.brightnesses[int(max(1, min(100, (self.pelvis_ang_vel - spin_min) / (spin_max - spin_min) * 100)))]


#class MyWindow(QMainWindow):
#    def __init__(self):
#        super().__init__()
#        #print(MySubscriber.color)
#        #print(MySubscriber.brightness)
#        #self.label = QLabel(str(my_subscriber.pelvis_ang_vel), self)
#        #self.setCentralWidget(self.label)
        
#        self.title = 'PyQt rectangle colors - pythonspot.com'
#        self.left = 0
#        self.top = 0
#        self.width = 860
#        self.height = 1080
#        #self.color = [0,0,0]
#        #self.brightnesses = [x for x in range(1,100,1)]
#        self.initUI()

#        self.timer = QTimer(self)
#        self.timer.timeout.connect(self.update_label)
#        self.timer.start(1000)  # Update the label every 100ms
        
#        self.setWindowTitle(self.title)
#        self.setGeometry(self.left, self.top, self.width, self.height)
        
#        # Set window background color
#        self.setAutoFillBackground(True)
#        p = self.palette()
#        p.setColor(self.backgroundRole(), Qt.white)
#        self.setPalette(p)
    
#    def initUI(self):
#        self.setWindowTitle(self.title)
#        self.setGeometry(self.left, self.top, self.width, self.height)
        
#        # Set window background color
#        self.setAutoFillBackground(True)
#        p = self.palette()
#        p.setColor(self.backgroundRole(), Qt.white)
#        self.setPalette(p)
#        #self.show()

#    def update_label(self):
#        #self.label.setText(str(my_subscriber.pelvis_ang_vel))
#        #self.brightnesses = [x for x in range(1,100,1)]
#        color = MySubscriber.color
#        color_rgb = QColor(color[0], color[1], color[2])
#        color_hsv = color_rgb.getHsv()
#        #brightness = MySubscriber.brigthness
#        print(color_rgb.getHsv(), color_hsv)
        
#        qp = QPainter(self)
        
#        qp.setBrush(QColor.fromHsv(color_hsv[0], 100, 255, 255))
#        qp.drawRect(0, 0, 1920, 1080)


#if __name__ == "__main__":
#    #rospy.init_node("my_node")
#    my_subscriber = MySubscriber()

#    app = QApplication([])
#    window = MyWindow()
#    window.show()
#    app.exec_()

