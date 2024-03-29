from matplotlib import pyplot as plt
import numpy as np
import os
import sys

np.set_printoptions(suppress=True)

# try:
#     data = np.loadtxt(sys.argv[1])
# except:
#     print("no data!!")
#     sys.exit()


field_x = [-90,-90,90,90,-90]
field_y = [-60,60,60,-60,-60]

for k in range(185):
    if k < 140:
        K = k*20
    else:
        K = k*5
    data = np.loadtxt('./datas/path_date_20191113_165603/plotdata_' + str(K+1).zfill(4) + '.txt')

    for i in range(len(data)):
        # print(data[i])
        print(K)
        plt.ion()
        plt.plot(data[i][2],data[i][3],marker='o',markersize=12.5,color="red",label="ball")
        plt.plot(data[i][0],data[i][1],marker="o",markersize=12.5,color='blue',label="robot")
        plt.plot(field_x,field_y,markersize=1,color="black")
        plt.plot(80,0,marker="X",color="green",label="goal")
        plt.legend(loc="lower right",prop={'size':10})
        plt.axes().set_aspect('equal')
        plt.draw()
        plt.pause(0.01)
        # if i == 0 or i == len(data)-1:input("press enter") 
        if k == 0 and i == 0 :input("press enter") 
        plt.cla()
