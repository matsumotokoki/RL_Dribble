from mujoco_py import load_model_from_path, MjSim, MjViewer
from mymjviewer import MyMjViewer
import numpy as np
import math
import random
import os
import sys
import glfw

# model = load_model_from_path("~/Downloads/darwin/darwin_OP.xml")
model = load_model_from_path("./xml/world5.xml")
sim = MjSim(model)
viewer = MyMjViewer(sim)
t=0

def norm_vec(vec):
    norm = np.linalg.norm(vec)
    vec = vec/norm
    return vec

while True:
    sim.step()
    robot_x, robot_y = sim.data.body_xpos[1][0:2]
    ball_x, ball_y = sim.data.body_xpos[2][0:2]
    vx = sim.data.qvel[0:2]
    ball_vel =  sim.data.qvel[2:4]
    ball_pos_local = -(robot_x - ball_x), -(robot_y - ball_y)
    # goal_arr = (-ball_y)/(-90 - ball_x)
    # goal_oriented_arr = (ball_vel[1])/(ball_vel[0])
    goal_arr = np.array([-90-ball_x,-ball_y])
    goal_oriented_arr = np.array([ball_vel[0],ball_vel[1]])
    goal_arr = norm_vec(goal_arr)
    goal_arr_deg = math.degrees(math.atan2(goal_arr[1],goal_arr[0]))
    goal_oriented_arr = norm_vec(goal_oriented_arr)
    goal_oriented_deg = math.atan2(goal_oriented_arr[1],goal_oriented_arr[0])
    goal_oriented_deg = math.degrees(goal_oriented_deg)
    distance = math.sqrt(ball_pos_local[0]**2 + ball_pos_local[1]**2)
    print("----------------------------")
    print("robot:    ",robot_x,robot_y)
    # print("ball:     ",ball_x,ball_y)
    # print("local:    ",ball_pos_local)
    # print("distance: ",distance)
    # print("robot_vel:",vx)
    # print("goa:      ",round(goal_oriented_arr,1))
    # print("ga:       ",round(goal_arr,1))
    # print("diff_arr: ",round(math.fabs(goal_arr-goal_oriented_arr),1))
    # print("goa:      ",goal_oriented_arr)
    print("goal_deg: ",goal_oriented_deg)
    # print("ga:       ",goal_arr)
    print("ga_deg:   ",goal_arr_deg)
    print("vel:      ",sim.data.qvel)
    print("vel:   ",round(sim.data.qvel[6],2))
    print("vel:   ",round(sim.data.qvel[7],2))
    # print("ball_vel: ",ball_vel)
    print("----------------------------")
    print()
    t+=1
    viewer.render()
    if ball_x > 80 and  -25< ball_y < 25: 
        print("reset!!")
        sim.reset()
