import numpy as np
import math
import pathlib
import sys

from core.base import Base
from core_ext.camera import Camera
from core_ext.mesh import Mesh
from core_ext.renderer import Renderer
from core_ext.scene import Scene
from extras.axes import AxesHelper
from extras.grid import GridHelper
from extras.movement_rig import MovementRig
from material.surface import SurfaceMaterial
from core.obj_reader import my_obj_reader  
from core.customGeometry import customGeometry  
from core.matrix import Matrix

class Example(Base):
    def initialize(self):
        print("Initializing program...")
        self.renderer = Renderer()
        self.scene = Scene()
        
        self.camera = Camera(aspect_ratio=800/600)
        self.camera.set_position([0.5, 1, 5])
        
        geometry = customGeometry(1, 1, 1, my_obj_reader('harmonic1.obj'))
        material = SurfaceMaterial(property_dict={"useVertexColors": True})
        self.mesh = Mesh(geometry, material)

        self.rig = MovementRig()
        self.rig.add(self.mesh)
        
        self.current_position = [0, 0.5, -0.5]
        self.rig.set_position(self.current_position)

        self.scene.add(self.rig)
        self.scene.add(AxesHelper(axis_length=2))
        
        grid = GridHelper(size=20, grid_color=[1, 1, 1], center_color=[1, 1, 0])
        grid.rotate_x(-math.pi / 2)
        self.scene.add(grid)

        self.movement_phase = 0
        self.movement_queue = []
        self.move_speed = 2.5
        self.target_x = None

    def start_movement_sequence(self):
        self.movement_queue = [1.5, -3.0, 1.5]
        self.target_x = self.current_position[0] + self.movement_queue[0]
        self.movement_phase = 1

    def execute_movement(self):
        if self.target_x is None or self.movement_phase == 0:
            return

        current_x = self.current_position[0]
        new_x = self.approach(current_x, self.target_x, self.move_speed * self.delta_time)
        self.current_position[0] = new_x
        self.rig.set_position(self.current_position)

        if abs(new_x - self.target_x) < 0.01:
            if self.movement_phase < len(self.movement_queue):
                self.movement_phase += 1
                self.target_x = self.target_x + self.movement_queue[self.movement_phase - 1]
            else:
                self.movement_phase = 0
                self.target_x = None

    def approach(self, current, target, delta):
        if current < target:
            return min(current + delta, target)
        else:
            return max(current - delta, target)

    def update(self):
        self.rig.update(self.input, self.delta_time)

        if self.input.is_key_pressed('x') and self.movement_phase == 0:
            self.start_movement_sequence()

        if self.movement_phase > 0:
            self.execute_movement()

        self.renderer.render(self.scene, self.camera)

Example(screen_size=[800, 600]).run()
