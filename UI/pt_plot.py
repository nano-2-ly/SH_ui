import sys
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

class MainDialog(QDialog):
    switch_window = QtCore.pyqtSignal()

    def __init__(self):

        QDialog.__init__(self, None)

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


        self.show()


class CWidget(QWidget):
     
    def __init__(self):
        super().__init__()
        # for PyQt embedding
        self.fig = plt.Figure()
        
        self.canvas = FigureCanvasQTAgg(self.fig)

        self.N = 50 # Meshsize
        self.fps = 100 # frame per sec
        self.frn = 100 # frame number of the animation

        self.x = np.linspace(-4,4,self.N+1)
        self.x, self.y = np.meshgrid(self.x, self.x)
        self.zarray = np.zeros((self.N+1, self.N+1, self.frn))
        
        for i in range(self.frn):
            self.zarray[:,:,i] = self.f(self.x,self.y,1.5+np.sin(i*2*np.pi/self.frn))

        self.initUI()
    
    def f(self, x, y, i):
        print(i)
        return np.sin(np.sqrt((x + i)** 2 + (y + i) ** 2))

    def initUI(self):
        vbox = QVBoxLayout()
        vbox.addWidget(self.canvas)
        
        
        b1 = QPushButton("Button1")
        vbox.addWidget(b1)
 
        self.setLayout(vbox)
        #self.setGeometry(0,0,800,400)
         
        # 1~1 중 1번째(1,1,1)  서브 챠트 생성
        self.ax = self.fig.add_subplot(111, projection='3d')         
        # 2D line
        self.plot = [self.ax.plot_surface(self.x, self.y, self.zarray[:,:,0], color='0.75', rstride=1, cstride=1)]
        self.ax.set_zlim(0,1.1)
        ani = animation.FuncAnimation(self.fig, self.update_plot, self.frn, fargs=(self.zarray, self.plot), interval=1000/self.fps)

        self.canvas.draw()
 
        #self.show()      
    def update_plot(self, frame_number, zarray, plot):
        self.plot[0].remove()
        self.plot[0] = self.ax.plot_surface(self.x, self.y, zarray[:,:,frame_number], cmap="hot")

 

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