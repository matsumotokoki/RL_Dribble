import numpy as np
from mujoco_py import load_model_from_path, MjSim, MjViewer
from mymjviewer import MyMjViewer
import random
import glfw
import time
import math

class Dribble_Env(object):
    def __init__(self):
        self.model = load_model_from_path("./xml/world3.xml") 
        self.sim = MjSim(self.model)
        # self.viewer = MyMjViewer(self.sim)
        self.viewer = MjViewer(self.sim)
        self.max_vel = [-1000,1000]
        self.x_motor = 0
        self.y_motor = 0

    def step(self,action):
        self.x_motor = np.clip(self.x_motor + ((action %3)-1) *100,-1000,1000)
        self.y_motor = np.clip(self.y_motor + ((action //3)-1) *100,-1000,1000)
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
        ball_pos_local = -(robot_x - ball_x), -(robot_y - ball_y)
        # distance = math.sqrt(ball_pos_local[0]**2 + ball_pos_local[1]**2)

        return [robot_x, robot_y, ball_pos_local[0], ball_pos_local[1], robot_xv, robot_yv, ball_x, ball_y]

    def check_done(self):
        ball_x ,ball_y = self.get_state()[6:]
        if ball_x < -80 and -25 < ball_y < 25:
            return True
        else:
            return False

    def reset(self):
        self.x_motor = 0
        self.y_motor = 0
        self.sim.reset()

    def render(self):
        self.viewer.render()
