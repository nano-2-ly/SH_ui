import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import serial
arr=[]
ser  = serial.Serial("COM3", baudrate= 115200, 
            timeout=2.5, 
            parity=serial.PARITY_NONE, 
            bytesize=serial.EIGHTBITS, 
            stopbits=serial.STOPBITS_ONE
            )

for i in range(100):
    c=np.random.rand(64,32)        
    arr.append(c)
fig = plt.figure()
i=0
im = plt.imshow(arr[0], animated=True, vmin=1, vmax=4)

def exp_filter(data):
    print(np.exp(data))
    return np.exp(data)

def updatefig(*args):
    im.set_array(exp_filter(receive_data()))
    return im,

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
ani = animation.FuncAnimation(fig, updatefig,  blit=True)
plt.show()