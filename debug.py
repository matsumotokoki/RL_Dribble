from mujoco_py import load_model_from_path, MjSim
from mymjviewer import MyMjViewer
import numpy as np
import math
import random
import os
import sys
import glfw

model = load_model_from_path("./xml/world.xml")
sim = MjSim(model)
viewer = MyMjViewer(sim)
t=0
while True:
    sim.step()
    t+=1
    viewer.render()
