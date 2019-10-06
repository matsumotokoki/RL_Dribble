from mujoco_py import load_model_from_path, MjSim, MjViewer
import numpy as np
import math
import random
import os
import sys
from pygame.locals import *
import pygame

model = load_model_from_path("./xml/world.xml")
sim = MjSim(model)
viewer = MjViewer(sim)
t=0
while True:
    sim.data.ctrl[0] = 30 * -math.cos(0.001 * t)  
    sim.data.ctrl[1] = 30 * -math.sin(0.001 * t)
    print(sim.data.body_xpos)
    sim.step()
    t+=1
    viewer.render()
