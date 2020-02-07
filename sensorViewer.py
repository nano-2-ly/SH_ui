import time
import json
import serial
from pprint import pprint
import random

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt



if __name__ == "__main__":
    print ("Ready...")
    ser  = serial.Serial("COM11", baudrate= 115200, 
        timeout=2.5, 
        parity=serial.PARITY_NONE, 
        bytesize=serial.EIGHTBITS, 
        stopbits=serial.STOPBITS_ONE
        )

    fig = plt.figure()
    ax = fig.add_subplot(111)
    im = ax.imshow(np.random.random((1,32)))
    plt.show(block=False)

    while True : 
        try:
            sensorValue = np.array([])
            for i in range(32) : 
                verify = ser.readline().decode().replace('\r\n','')
                a = str(verify).split()
                print(verify)
                np.append(sensorValue

                

                time.sleep(1)
                im.set_array(np.array(a).astype(np.float).reshape([1,32])/4096)
                # redraw the figure
                fig.canvas.draw()
        except :
            print('error')
            pass