import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLabel
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import random

# adapted from https://pythonspot.com/pyqt5-colors/

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'PyQt rectangle colors - pythonspot.com'
        self.left = 0
        self.top = 0
        self.width = 860
        self.height = 1080
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        # Set window background color
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.white)
        self.setPalette(p)
        
        # Add paint widget and paint
        self.m = PaintWidget(self)
        self.m.move(0,0)
        self.m.resize(self.width,self.height)
        
        self.show()
    
class PaintWidget(QWidget):
    def paintEvent(self, event):
        qp = QPainter(self)
        
        qp.setPen(Qt.black)
        size = self.size()
        
        # Colored rectangles
        color = [200, 0, 0]
        color_rgb = QColor(color[0], color[1], color[2])
        color_hsv = (color_rgb).getHsv()
        print(color_rgb.getHsv(), color_hsv)
        brightness = 100
        qp.setBrush(QColor.fromHsv(color_hsv[0], brightness, 255, 255))
        qp.drawRect(0, 0, 1920, 1080)
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
