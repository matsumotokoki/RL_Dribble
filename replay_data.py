from matplotlib import pyplot as plt
import numpy as np
import os
import sys

np.set_printoptions(suppress=True)

try:
    data = np.loadtxt(sys.argv[1])
except:
    print("no data!!")
    sys.exit()


field_x = [-90,-90,90,90,-90]
field_y = [-60,60,60,-60,-60]
for i in range(len(data)):
    print(data[i])
    fig1 = plt.figure()
    plt.ion()
    plt.show()
    plt.plot(data[i][2],data[i][3],marker='o',markersize=8,color="red",label="ball")
    plt.plot(data[i][0],data[i][1],marker="o",markersize=8,color='blue',label="robot")
    plt.plot(field_x,field_y,markersize=1,color="black")
    plt.plot(80,0,marker="X",color="green",label="goal")
    plt.legend(loc="lower right")
    # plt.axes().set_aspect('equal')
    plt.draw()
    plt.pause(0.01)
    plt.close(1)
