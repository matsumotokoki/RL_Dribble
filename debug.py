from mujoco_py import load_model_from_path, MjSim, MjViewer
import numpy as np
import math
import random
import os
import sys
import glfw

class MyMjViewer(MjViewer):
    def __init__(self, sim):
        super().__init__(sim)
        self.sim = sim
        
    def key_callback(self, window, key, scancode, action, mods):
        if action != glfw.RELEASE:
            return
        elif key == glfw.KEY_TAB:  # Switches cameras.
            self.cam.fixedcamid += 1
            self.cam.type = const.CAMERA_FIXED
            if self.cam.fixedcamid >= self._ncam:
                self.cam.fixedcamid = -1
                self.cam.type = const.CAMERA_FREE
        # elif key == glfw.KEY_H:  # hides all overlay.
        #     self._hide_overlay = not self._hide_overlay
        elif key == glfw.KEY_SPACE and self._paused is not None:  # stops simulation.
            self._paused = not self._paused
        # Advances simulation by one step.
        elif key == glfw.KEY_RIGHT and self._paused is not None:
            self._advance_by_one_step = True
            self._paused = True
        elif key == glfw.KEY_V or \
                (key == glfw.KEY_ESCAPE and self._record_video):  # Records video. Trigers with V or if in progress by ESC.
            self._record_video = not self._record_video
            if self._record_video:
                fps = (1 / self._time_per_render)
                self._video_process = Process(target=save_video,
                                  args=(self._video_queue, self._video_path % self._video_idx, fps))
                self._video_process.start()
            if not self._record_video:
                self._video_queue.put(None)
                self._video_process.join()
                self._video_idx += 1
        elif key == glfw.KEY_T:  # capture screenshot
            img = self._read_pixels_as_in_window()
            imageio.imwrite(self._image_path % self._image_idx, img)
            self._image_idx += 1
        elif key == glfw.KEY_I:  # drops in debugger.
            print('You can access the simulator by self.sim')
            import ipdb
            ipdb.set_trace()
        elif key == glfw.KEY_S:  # Slows down simulation.
            self._run_speed /= 2.0
        elif key == glfw.KEY_F:  # Speeds up simulation.
            self._run_speed *= 2.0
        elif key == glfw.KEY_C:  # Displays contact forces.
            vopt = self.vopt
            vopt.flags[10] = vopt.flags[11] = not vopt.flags[10]
        elif key == glfw.KEY_D:  # turn off / turn on rendering every frame.
            self._render_every_frame = not self._render_every_frame
        elif key == glfw.KEY_E:
            vopt = self.vopt
            vopt.frame = 1 - vopt.frame

        elif key == glfw.KEY_L:
            self.sim.data.ctrl[0] += 100 if self.sim.data.ctrl[0] < 500 else 0
            print("right")
        elif key == glfw.KEY_H:
            self.sim.data.ctrl[0] += -100 if self.sim.data.ctrl[0] > -500 else 0
            self._hide_overlay = True
            print("left")
        elif key == glfw.KEY_K:
            self.sim.data.ctrl[1] += 100 if self.sim.data.ctrl[0] < 500 else 0
            print("up")
        elif key == glfw.KEY_J:
            self.sim.data.ctrl[1] += -100 if self.sim.data.ctrl[0] > -500 else 0
            print("down")
        elif key == glfw.KEY_N:
            self.sim.data.ctrl[0] = 0
            self.sim.data.ctrl[1] = 0
            print("stop")
        
        elif key == glfw.KEY_R:  # makes everything little bit transparent.
            self._transparent = not self._transparent
            if self._transparent:
                self.sim.model.geom_rgba[:, 3] /= 5.0
            else:
                self.sim.model.geom_rgba[:, 3] *= 5.0
        elif key == glfw.KEY_M:  # Shows / hides mocap bodies
            self._show_mocap = not self._show_mocap
            for body_idx1, val in enumerate(self.sim.model.body_mocapid):
                if val != -1:
                    for geom_idx, body_idx2 in enumerate(self.sim.model.geom_bodyid):
                        if body_idx1 == body_idx2:
                            if not self._show_mocap:
                                # Store transparency for later to show it.
                                self.sim.extras[
                                    geom_idx] = self.sim.model.geom_rgba[geom_idx, 3]
                                self.sim.model.geom_rgba[geom_idx, 3] = 0
                            else:
                                self.sim.model.geom_rgba[
                                    geom_idx, 3] = self.sim.extras[geom_idx]
        elif key in (glfw.KEY_0, glfw.KEY_1, glfw.KEY_2, glfw.KEY_3, glfw.KEY_4):
            self.vopt.geomgroup[key - glfw.KEY_0] ^= 1
        super().key_callback(window, key, scancode, action, mods)

model = load_model_from_path("./xml/world.xml")
sim = MjSim(model)
viewer = MyMjViewer(sim)
t=0
while True:
    # sim.data.ctrl[0] = 300 * -math.cos(0.01 * t)  
    # sim.data.ctrl[1] = 300 * -math.sin(0.01 * t)
    print(sim.data.ctrl)
    sim.step()
    t+=1
    viewer.render()
