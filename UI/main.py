import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout ,QPushButton, QHBoxLayout, QLineEdit, QLabel, QSlider, QSpacerItem, QComboBox
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import numpy as np
from PyQt5.QtGui import QPainter,QColor
from PyQt5.QtGui import QPainter, QBrush, QPen
import serial.tools.list_ports
import csv
import datetime

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
 
class CWidget(QWidget):
     
    def __init__(self):
        super().__init__()
        self.arr=[]
        
        for i in range(5):
            c=np.random.rand(64,32)
            self.arr.append(c)
        # for PyQt embedding
        self.fig = plt.Figure()
        self.ax = self.fig.add_subplot(111)      
        self.im = self.ax.imshow(self.arr[0], animated=True, vmin=-1, vmax=300)
        self.canvas = FigureCanvasQTAgg(self.fig)
        

 
        self.timeInterval = 0.1
        
                
        self.initUI()
 
    def initUI(self):

        self.menu = QVBoxLayout()

        self.combo_label = QLabel(self)
        self.combo_label.setText('Port')
        self.combo_label.setAlignment(Qt.AlignCenter)
        self.combo_label.setStyleSheet("QLabel { background-color: #2E3D50;color:#ffffff; border: none; font-weight: regular; font-size: 15pt;font-family: Calibri;}")
        

        self.combo = QComboBox(self)
        self.ports = list(serial.tools.list_ports.comports())
        for p in self.ports:
            self.combo.addItem(p[0])


        self.sense_label = QLabel(self)
        self.sense_label.setText('Sensitivity')
        self.sense_label.setAlignment(Qt.AlignCenter)
        self.sense_label.setStyleSheet("QLabel { background-color: #2E3D50;color:#ffffff; border: none; font-weight: regular; font-size: 15pt;font-family: Calibri;}")
        
        self.threshold_label = QLabel(self)
        self.threshold_label.setText('Threshold')
        self.threshold_label.setAlignment(Qt.AlignCenter)
        self.threshold_label.setStyleSheet("QLabel { background-color: #2E3D50;color:#ffffff; border: none; font-weight: regular; font-size: 15pt;font-family: Calibri;}")

        self.save_button = QPushButton("save")
        self.save_button.resize(260, 464)
        #self.save_button.move(150,50)
        self.save_button.setStyleSheet("""
            QPushButton { background-color: #2E3D50;color:#ffffff; border:  1px solid white; font-weight: regular; font-size: 15pt;font-family: Calibri;}
            QPushButton:hover{ background-color: #2E3D50; color:#ffffff;border: 3px solid white; font-weight: bold; font-size: 15pt;font-family: Calibri;}
            """)
        # self.logo_button.setStyleSheet("QPushButton{image:url(./image/logo.png); border:0px;}")

        self.sense_value = QLineEdit("100")
        self.sense_value.setAlignment(Qt.AlignCenter)
        self.sense_value.resize(260, 464)
        #self.option_button.move(150,50)
        #self.option_button.setStyleSheet("QPushButton { background-color: #2E3D50;color:#ffffff; border: none; font-weight: regular; font-size: 15pt;font-family: Calibri;}")
        
        self.sense_slider = QSlider(Qt.Horizontal) 
        self.sense_slider.setRange(1, 100)
        

        self.threshold_value = QLineEdit("0")
        self.threshold_value.setAlignment(Qt.AlignCenter)
        self.threshold_value.resize(260, 464)

        self.threshold_slider = QSlider(Qt.Horizontal) 
        self.threshold_slider.setRange(0, 100)
        

        #self.verticalSpacer = QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)

        self.menu.addWidget(self.combo_label)
        self.menu.addWidget(self.combo)
        
        self.menu.addSpacing(10)
        self.menu.addWidget(self.sense_label)
        self.menu.addWidget(self.sense_value)
        self.menu.addWidget(self.sense_slider)
        self.menu.addWidget(self.threshold_label)
        self.menu.addWidget(self.threshold_value)
        self.menu.addWidget(self.threshold_slider)
        self.menu.addSpacing(50)
        self.menu.addWidget(self.save_button)

        self.menu.setSpacing(0)
        self.menu.setContentsMargins(0,0,0,0)
        #self.menu.addStretch()
        self.menu.setAlignment(Qt.AlignVCenter)


        vbox = QHBoxLayout()
        vbox.setStretchFactor(self.menu, 5)
        vbox.setStretchFactor(self.canvas, 1)
        vbox.addLayout(self.menu)
        vbox.addWidget(self.canvas)

        self.save_button.clicked.connect(self.save_csv)
        self.threshold_slider.setValue(0)
        self.threshold_slider.valueChanged.connect(self.threshold_slider_value_changed)
        self.threshold_value.textChanged.connect(self.threshold_value_changed)
        
        self.sense_slider.setValue(100)
        self.sense_slider.valueChanged.connect(self.sense_slider_value_changed)
        self.sense_value.textChanged.connect(self.sense_value_changed)

        self.combo.currentTextChanged.connect(self.onChanged)    
        #self.combo.highlighted.connect(self.onClicked) 

        self.setLayout(vbox)
        self.setGeometry(0,0,800,800)
         
        # 1~1 중 1번째(1,1,1)  서브 챠트 생성
        # self.ax = self.fig.add_subplot(1,1,1)           
        # # 2D line
        # self.line, = self.ax.plot(self.x, self.y)        
 
        # 애니메이션 챠트 생성
        #self.ani = animation.FuncAnimation(self.fig, self.updatefig, blit=True)
        #self.canvas.draw()
        print(self.canvas.size())
        self.ani = animation.FuncAnimation(self.fig, self.updatefig, blit=True)
        self.canvas.draw()
        self.show()   

    def save_csv(self,):
        f = open('./data/{}.csv'.format(datetime.datetime.now().strftime("%m-%d-%Y-%H-%M-%S")), 'w', encoding='utf-8', newline='')
        wr = csv.writer(f)

        for i in range(64):
            wr.writerow(self.data[i])


    def onChanged(self, text):
        self.ser  = serial.Serial("COM3", baudrate= 115200, 
            timeout=2.5, 
            parity=serial.PARITY_NONE, 
            bytesize=serial.EIGHTBITS, 
            stopbits=serial.STOPBITS_ONE
            )
        
        self.ani = animation.FuncAnimation(self.fig, self.updatefig, blit=True)
        self.canvas.draw()

        

    def onClicked(self):
        self.ports = list(serial.tools.list_ports.comports())
        self.combo.clear()
        for p in self.ports:
            self.combo.addItem(p[0])

    def paintEvent(self, event):
        height = self.size().height() 
        width = self.size().width()
        painter = QPainter(self)

        painter.setPen(QPen(QColor(46,61,80),  5, Qt.SolidLine))
        painter.setBrush(QBrush(QColor(46,61,80), Qt.SolidPattern))
        #painter.drawRect(0, 0, width-self.canvas.size().width() , height)
        painter.drawRect(0, 0, width, height)
    
    def threshold_value_changed(self):
        try:
            if self.threshold_value.text() == '':
                self.threshold_slider.setValue(1)
            elif self.threshold_value.text() == '0':
                self.threshold_slider.setValue(1)
            else:
                self.threshold_slider.setValue(int(self.threshold_value.text()))
        except:
            self.threshold_slider.setValue(1)

    def threshold_slider_value_changed(self):
        self.threshold_value.setText(str(self.threshold_slider.value()))
        #print(self.threshold_slider.value())

    def sense_value_changed(self):
        try:
            if self.sense_value.text() == '':
                self.sense_slider.setValue(1)
            else:
                self.sense_slider.setValue(int(self.sense_value.text()))
        except:
            self.sense_slider.setValue(0)
    def sense_slider_value_changed(self):
        self.sense_value.setText(str(self.sense_slider.value()))
        #print(self.sense_slider.value())

    def closeEvent(self, e):
        pass

    def receive_data():
        temp = 0
        while True:
            data = ser.readline().decode("utf-8")

            data = str(data).replace('\r\n', ' ').split(' ')[:-3]
            
            data[1:] = list(map(int, data[1:]))
            data[1:] = np.divide(data[1:],100)
            
            try : 
                #print(data_set)
                pass
            except : 
                pass


            if 'a' in data:
                data_set = np.array(data[1:])
                temp = 1

            elif 'b' in data and temp==1:
                data_set = np.vstack([data_set, data[1:]])

            elif 'c' in data and temp==1:
                data_set = np.vstack([data_set, data[1:]])
                #print(data_set.shape)
                return data_set

            #else :
            #    print(data)

    def updatefig(self,*args):
        #c= receive_data()
        #print('hi')
        c = np.random.randn(64,32)
        c = self.Sensitivity(c)
        c = self.Threshold(c)
        self.data = c  
        self.im.set_array(self.data)
        return self.im,

    def Sensitivity(self, data):
        return np.power(self.sense_slider.value(), data)

    def Threshold(self, data):
        data[data <= self.threshold_slider.value()] = 0
        return data

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = CWidget()
    sys.exit(app.exec_())