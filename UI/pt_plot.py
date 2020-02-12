import sys
import serial
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QMainWindow, QPushButton
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import numpy as np
from mpl_toolkits.mplot3d import Axes3D 
#QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QPainter,QColor
from PyQt5.QtGui import QPainter, QBrush, QPen
 

class MainDialog(QDialog):
    switch_window = QtCore.pyqtSignal()

    def __init__(self):

        QDialog.__init__(self, None)

        width = 0
        height = 0  

        qp = QPainter()
        qp.begin(self)           
        qp.drawRect(0, 0, width, height)        
        qp.end()

        self.logo_button = QPushButton(self)
        self.logo_button.resize(260, 464)
        self.logo_button.move(150,50)
        self.logo_button.setStyleSheet("QPushButton{image:url(./image/logo.png); border:0px;}")

        self.team_logo_button = QPushButton(self)
        self.team_logo_button.resize(100, 25)
        self.team_logo_button.move(0,0)
        self.team_logo_button.setStyleSheet("QPushButton{image:url(./image/team_logo.png); border:0px;}")


        self.enter_button = QPushButton(self)
        self.enter_button.resize(144, 46)
        self.enter_button.move(208,450)
        self.enter_button.setStyleSheet(
            """
            QPushButton{image:url(./image/enter.png); border:0px;}
            QPushButton:hover{image:url(./image/enter_hover.png); border:0px;}
                    
            """)


        self.enter_button.clicked.connect(self.enter)
        

        self.setStyleSheet("QDialog{background: 'white';}")
        self.resize(560,680)
        self.show()
    
    def enter(self):
        self.switch_window.emit()


class MainApp(QMainWindow):
    """This is the class of the MainApp GUI system"""
    def __init__(self):
        """Constructor method that inherits methods from QWidgets"""
        super().__init__()
        self.initUI()

    def initUI(self):

        #page = QHBoxLayout()
        btn_layout = QHBoxLayout()
        canvas_layout = QHBoxLayout()
        layout = QHBoxLayout()
        
        b1 = QPushButton("Button1")

        btn_layout.addWidget(b1)



        centralWidget= CWidget()
        canvas_layout.addWidget(centralWidget)
        
        self.setCentralWidget(centralWidget)

        self.resize(560,680)
        self.show()


class CWidget(QWidget):
     
    def __init__(self):
        super().__init__()
        # for PyQt embedding
        self.fig = plt.Figure(figsize=(100, 50))
        
        self.canvas = FigureCanvasQTAgg(self.fig)

        self.row =  64# Meshsize
        self.col = 32
        self.fps = 1000 # frame per sec
        self.frn = 10 # frame number of the animation

        self.x = np.linspace(-4,4,self.col)
        self.y = np.linspace(-4,4,self.row)
        self.x, self.y = np.meshgrid(self.x, self.y)
        
        self.zarray = np.zeros([64,32])


        self.ser  = serial.Serial("COM4", baudrate= 115200, 
            timeout=2.5, 
            parity=serial.PARITY_NONE, 
            bytesize=serial.EIGHTBITS, 
            stopbits=serial.STOPBITS_ONE
            )

        self.initUI()


    def paintEvent(self, event):
        height = self.size().height() 
        width = self.size().width()
        painter = QPainter(self)

        painter.setPen(QPen(QColor(46,61,80),  5, Qt.SolidLine))
        painter.setBrush(QBrush(QColor(46,61,80), Qt.SolidPattern))
        painter.drawRect(0, 0, width/4.4, height)
    
    def f(self, x, y, i):
        print(i)
        return np.sin(np.sqrt((x + i)** 2 + (y + i) ** 2))

    def initUI(self):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.black, 5, Qt.SolidLine))
        #painter.setBrush(QBrush(Qt.red, Qt.SolidPattern))
        painter.setBrush(QBrush(Qt.green, Qt.DiagCrossPattern))
        painter.drawRect(100, 15, 400 ,200)
        
        
        layout = QVBoxLayout()


        vbox = QHBoxLayout()
        vbox.setSpacing(20)

        menu = QVBoxLayout()
        menu.setAlignment(QtCore.Qt.AlignCenter)
        menu.setSpacing(40)

        b1 = QPushButton("save")
        b1.setStyleSheet("QPushButton { background-color: #2E3D50;color:#ffffff; border: none; font-weight: regular; font-size: 15pt;font-family: Calibri;}")
        menu.addWidget(b1)
        b2 = QPushButton("reset")
        b2.setStyleSheet("QPushButton { background-color: #2E3D50;color:#ffffff; border: none; font-weight: regular; font-size: 15pt;font-family: Calibri;}")
        menu.addWidget(b2)
        b3 = QPushButton("connect")
        b3.setStyleSheet("QPushButton { background-color: #2E3D50;color:#ffffff; border: none; font-weight: regular; font-size: 15pt;font-family: Calibri;}")
        menu.addWidget(b3)
        b4 = QPushButton("option")
        b4.setStyleSheet("QPushButton { background-color: #2E3D50;color:#ffffff; border: none; font-weight: regular; font-size: 15pt;font-family: Calibri;}")
        menu.addWidget(b4)

        
        vbox.addLayout(menu)
        vbox.setStretchFactor(menu, 1)
        
        vbox.addWidget(self.canvas)
        vbox.setStretchFactor(self.canvas, 4)
        self.setLayout(vbox)

        status = QLineEdit()
        layout.addWidget(status)
        layout.addLayout(vbox)
        
        layout.setStretchFactor(vbox, 1)
        layout.setStretchFactor(status, 4)
        self.setLayout(layout)

        #self.setGeometry(0,0,800,400)
         
        # 1~1 중 1번째(1,1,1)  서브 챠트 생성
        self.ax = self.fig.add_subplot(111, projection='3d')         
        # 2D line
        self.plot = [self.ax.plot_surface(self.x, self.y, self.zarray, color='0.75', rstride=1, cstride=1)]
        self.ax.set_zlim(0,1.1)
        ani = animation.FuncAnimation(self.fig, self.update_plot, interval=1000/self.fps)

        self.canvas.draw()
 
        #self.show()      
    def update_plot(self,frame_number):
        self.plot[0].remove()
        #self.plot[0] = self.ax.plot_surface(self.x, self.y, zarray[:,:,frame_number], cmap="hot")
        #self.plot[0] = self.ax.plot_surface(self.x, self.y, zarray[:,:,frame_number], cmap="viridis")

        self.plot[0] = self.ax.plot_surface(self.x, self.y, self.receive_data(), cmap="viridis")

    def receive_data(self):
        while True:
            data = self.ser.readline().decode("utf-8")
            data = str(data).replace('\r\n', '').split(' ')
            data[:-1] = list(map(int, data[:-1]))
            data[:-1] = np.divide(data[:-1],100)
            print(data)
            try : 
                print(data_set)
            except : 
                pass
            print( ' ')
            print( ' ')
            print( ' ')

            if 'a' in data:
                data_set = np.array(data[:-1])

            elif 'b' in data:
                data_set = np.vstack([data_set, data[:-1]])

            elif 'c' in data:
                data_set = np.vstack([data_set, data[:-1]])
                return data_set

            else :
                print(data)


    def closeEvent(self, e):
        pass



class Controller:

    def __init__(self):
        self.show_main()

    def show_main(self):
        self.window = MainDialog()
        self.window.switch_window.connect(self.show_command)
        try :
            self.window_command.close()
            self.window.show()
        except :
            self.window.show()

    def show_command(self):
        self.window_command = MainApp()
        #self.window_command.switch_window.connect(self.show_main)
        self.window.close()
        self.window_command.show()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Controller()
    sys.exit(app.exec_())