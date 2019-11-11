import numpy as np
from mujoco_py import load_model_from_path, MjSim, MjViewer
from mymjviewer import MyMjViewer
from matplotlib import pyplot as plt
import random
import glfw
import time
import math
import os
import datetime

class Dribble_Env(object):
    def __init__(self):
        self.model = load_model_from_path("./xml/world3.xml") 
        self.sim = MjSim(self.model)
        # self.viewer = MyMjViewer(self.sim)
        self.viewer = MyMjViewer(self.sim)
        self.max_vel = [-1000,1000]
        self.x_motor = 0
        self.y_motor = 0
        self.date_time = datetime.datetime.now()
        self.path = "./datas/path_date" + str(self.date_time.strftime("_%Y%m%d_%H%M%S"))
        os.mkdir(self.path)

    def step(self,action):
        # self.x_motor = np.clip(self.x_motor + ((action %3)-1) *100,-500,500)
        # self.y_motor = np.clip(self.y_motor + ((action //3)-1) *100,-500,500)
        self.x_motor = ((action %3)-1) * 200
        self.y_motor = ((action//3)-1) * 200
        self.sim.data.ctrl[0] = self.x_motor 
        self.sim.data.ctrl[1] = self.y_motor
        # print("---------------------")
        # print(self.x_motor,self.y_motor,action)
        # print(self.sim.data.ctrl)
        self.sim.step()

    def get_state(self):
        robot_x, robot_y = self.sim.data.body_xpos[1][0:2]
        # TODO
        robot_xv, robot_yv = self.sim.data.qvel[0:2]
        ball_x, ball_y = self.sim.data.body_xpos[2][0:2]
        ball_xv, ball_yv = self.sim.data.qvel[2:4]
        ball_pos_local = -(robot_x - ball_x), -(robot_y - ball_y)
        # distance = math.sqrt(ball_pos_local[0]**2 + ball_pos_local[1]**2)

        return [robot_x, robot_y, ball_pos_local[0], ball_pos_local[1], \
                robot_xv, robot_yv, ball_x, ball_y,ball_xv,ball_yv]

    def check_done(self):
        ball_x ,ball_y = self.get_state()[6:8]
        if ball_x > 80 and -25 < ball_y < 25:
            return True
        else:
            return False

    def reset(self):
        self.x_motor = 0
        self.y_motor = 0
        self.robot_x_data = []
        self.robot_y_data = []
        self.ball_x_data = []
        self.ball_y_data = []
        self.sim.reset()
        self.sim.data.qpos[0] = np.random.randint(-3,3)
        self.sim.data.qpos[1] = np.random.randint(-3,3)

    def render(self):
        self.viewer.render()

    def plot_data(self,step,t,done,episode,flag):
        self.field_x = [-90,-90,90,90,-90]
        self.field_y = [-60,60,60,-60,-60]
        self.robot_x_data.append(self.sim.data.body_xpos[1][0])
        self.robot_y_data.append(self.sim.data.body_xpos[1][1])
        self.ball_x_data.append(self.sim.data.body_xpos[2][0])
        self.ball_y_data.append(self.sim.data.body_xpos[2][1])

        datas = str(self.robot_x_data[-1])+" "+str(self.robot_y_data[-1])+" "+str(self.ball_x_data[-1])+" "+str(self.ball_y_data[-1])
        with open(self.path + '/plotdata_' + str(episode+1).zfill(4)+ '.txt','a') as f:
            f.write(str(datas)+'\n')
        
        if (t >= step-1 or done) and flag:
            fig1 = plt.figure()
            plt.ion()
            plt.show()
            plt.plot(self.ball_x_data,self.ball_y_data,marker='o',markersize=2,color="red",label="ball")
            plt.plot(self.robot_x_data,self.robot_y_data,marker="o",markersize=2,color='blue',label="robot")
            plt.plot(self.field_x,self.field_y,markersize=1,color="black")
            plt.plot(80,0,marker="X",color="green",label="goal")
            plt.legend(loc="lower right")
            # plt.axes().set_aspect('equal')
            plt.draw()
            plt.pause(0.001)
            plt.close(1)
