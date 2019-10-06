from mujoco_py import load_model_from_path, MjSim, MjViewer
import numpy as np
import math
import random
import os
import sys
from pygame.locals import *
import pygame

pygame.init()    # Pygameを初期化
screen = pygame.display.set_mode((10, 10))    # 画面を作成
model = load_model_from_path("./xml/world.xml")
sim = MjSim(model)
viewer = MjViewer(sim)
ctrl_val = [0,0]

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:  # キーを押したとき
            # ESCキーならスクリプトを終了
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            
            elif str(pygame.key.name(event.key)) == "k":
                print("押されたキー = " + pygame.key.name(event.key))
                ctrl_val = [0,0.1]
            elif str(pygame.key.name(event.key)) == "j":
                print("押されたキー = " + pygame.key.name(event.key))
                ctrl_val = [0,-0.1]
            elif str(pygame.key.name(event.key)) == "l":
                print("押されたキー = " + pygame.key.name(event.key))
                ctrl_val = [0.1,0]
            elif str(pygame.key.name(event.key)) == "h":
                print("押されたキー = " + pygame.key.name(event.key))
                ctrl_val = [-0.1,0]
            else:
                ctrl_cal = [0,0]
                print("non")

    if ctrl_val[0]:
        sim.data.ctrl[0] = ctrl_val[0]  
    else:
        sim.data.ctrl[0] = 0
    
    if ctrl_val[1]:
        sim.data.ctrl[1] = ctrl_val[1]
    else:
        sim.data.ctrl[1] = 0
    # print(sim.data.ctrl)
    sim.step()
    viewer.render()
