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
import rospy
from std_msgs.msg import Int32
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtCore import QTimer
import colour as Color

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
        self.red = Color.Color("red")
        self.colors = list(self.red.range_to(Color.Color("blue"),100))
        color_var = max(1, min(100, (y_pos - y_min) / (y_max - y_min) * 100))
        color = self.colors[int(color_var)]
        color = [int(x*255) for x in color.rgb]
        color_rgb = QColor(color[0], color[1], color[2])
        color_hsv = color_rgb.getHsv()
        #self.color = [int(x*255) for x in color.rgb]
        self.color = color_hsv[0]
        #print(self.x_pos,self.y_pos)
    
    def xsens_angular_moments_callback(self, data):
        self.xsens_angular_moment = numpy.array(data.data)
        self.pelvis_ang_vel = abs(self.xsens_angular_moment[4])
        #print(abs(self.xsens_angular_moment[4]))
        spin_max = 200
        spin_min = 0
        range_spin = 125
        if self.pelvis_ang_vel > spin_max:
            self.pelvis_ang_vel = spin_max
        self.brightnesses = [x for x in range(255-range_spin,255,1)]
        self.brightness = self.brightnesses[int(max(1, min(1, (self.pelvis_ang_vel - spin_min) / (spin_max - spin_min) * range_spin)))]


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        color = my_subscriber.color
        brightness = my_subscriber.brightness
        self.output = str(color) + ',' + str(brightness)
        self.label = QLabel(self.output, self)
        self.setCentralWidget(self.label)

        self.title = 'PyQt rectangle colors - pythonspot.com'
        self.left = 0
        self.top = 0
        self.width = 860
        self.height = 1080
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        # Set window background color
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.white)
        self.setPalette(p)
        
        #self.qp = QPainter(self)
        #self.qp.move(0,0)
        #self.qp.resize(self.width,self.height)
        #self.qp.setPen(Qt.black)
        #self.qp.setBrush(QColor.fromHsv(255, brightness,255,255))
        #self.qp.drawRect(0, 0, 860, 1920)
        
        # Add paint widget and paint
        self.m = PaintWidget(self)
        self.m.move(0,0)
        self.m.resize(self.width,self.height)
        self.show()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_label)
        self.timer.start(10)  # Update the label every 100ms

    def update_label(self):
        color = my_subscriber.color
        brightness = my_subscriber.brightness
        output = str(color) + ',' + str(brightness)
        self.label.setText(output)
        
        #self.qp = QPainter(self)
        #self.qp.setPen(Qt.black)
        #self.qp.drawRect(0, 0, 860, 1920)
        #self.show()
        
class PaintWidget(QWidget):
    def paintEvent(self, event):
        qp = QPainter(self)
        
        qp.setPen(Qt.black)
        size = self.size()
        color = my_subscriber.color
        brightness = my_subscriber.brightness
        
        # Colored rectangles
        qp.setBrush(QColor.fromHsv(color, brightness,255,255))
        qp.drawRect(0, 0, 860, 1920)

if __name__ == "__main__":
    rospy.init_node("my_node")
    my_subscriber = MySubscriber()

    app = QApplication([])
    window = MyWindow()
    window.show()
    app.exec_()
    


