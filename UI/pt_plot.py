import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QMainWindow, QPushButton
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import numpy as np
from mpl_toolkits.mplot3d import Axes3D 
#QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *



class MainApp(QMainWindow):
    """This is the class of the MainApp GUI system"""
    def __init__(self):
        """Constructor method that inherits methods from QWidgets"""
        super().__init__()
        self.initUI()

    def initUI(self):

        page = QHBoxLayout()
        control = QHBoxLayout()
        viewer = QHBoxLayout()
        
        '''
        b1 = QPushButton("Button1")
        b1.setLayout(control)

        centralwidget = CWidget()
        centralwidget.setLayout(viewer)
        self.setCentralWidget(centralwidget)
        '''

        b1 = CWidget()
        control.addWidget(b1)

        centralwidget = CWidget()
        control.addWidget(b1)
        self.setCentralWidget(centralwidget)
        self.setLayout(control)
        self.setLayout(viewer)

        
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
         
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainApp()
    sys.exit(app.exec_())