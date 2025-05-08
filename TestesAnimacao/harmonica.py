import numpy as np
import math
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
        
        self.rig.set_position([0, 0.5, -0.5])
        
        self.scene.add(self.rig)
        self.scene.add(AxesHelper(axis_length=2))
        
        grid = GridHelper(size=20, grid_color=[1, 1, 1], center_color=[1, 1, 0])
        grid.rotate_x(-math.pi / 2)
        self.scene.add(grid)

        self.animation_active = False
        self.current_animation = None
        self.animation_start_time = 0
        self.animation_duration = 2.0
        self.animation_speed = 2.5 
        self.animation_start_position = [0, 0.5, -0.5]
        
        self.animations = {
            'q': {'direction': [1.0, 0.0, 0.0], 'intensity': 1.5},
            'w': {'direction': [-1.0, 0.0, 0.0], 'intensity': 1.0},
            'e': {'direction': [0.0, 1.0, 0.0], 'intensity': 0.8},
            'r': {'direction': [0.0, -1.0, 0.0], 'intensity': 0.5},
            't': {'direction': [0.0, 0.0, 1.0], 'intensity': 1.2},
            'y': {'direction': [0.0, 0.0, -1.0], 'intensity': 1.0},
            'u': {'direction': [1.0, 1.0, 0.0], 'intensity': 0.7},
            'i': {'direction': [-1.0, 1.0, 0.0], 'intensity': 0.9},
            'o': {'direction': [0.5, 0.0, 0.5], 'intensity': 1.1},
            'p': {'direction': [-0.5, 0.0, -0.5], 'intensity': 1.3},
            '[': {'direction': [0.0, 0.5, 0.5], 'intensity': 0.6}
        }

    def start_animation(self, key):
        if key in self.animations:
            self.animation_start_position = self.rig.get_position()
            self.animation_active = True
            self.current_animation = key
            self.animation_start_time = self.time
            print(f"Animation {key} started")

    def update_animation(self, delta_time):
        if not self.animation_active or not self.current_animation:
            return

        elapsed = (self.time - self.animation_start_time) * self.animation_speed
        
        if elapsed > self.animation_duration:
            self.animation_active = False
            self.rig.set_position(self.animation_start_position)
            print(f"Animation {self.current_animation} completed")
            return

        progress = elapsed / self.animation_duration
        
        movement_progress = math.sin(progress * math.pi)
        
        anim_params = self.animations[self.current_animation]
        direction = anim_params['direction']
        intensity = anim_params['intensity']

        displacement = [
            direction[0] * intensity * movement_progress,
            direction[1] * intensity * movement_progress,
            direction[2] * intensity * movement_progress
        ]
        
        new_position = [
            self.animation_start_position[0] + displacement[0],
            self.animation_start_position[1] + displacement[1],
            self.animation_start_position[2] + displacement[2]
        ]
        
        self.rig.set_position(new_position)

    def update(self):
        self.rig.update(self.input, self.delta_time)

        for key in self.animations:
            if self.input.is_key_pressed(key) and not self.animation_active:
                self.start_animation(key)

        self.update_animation(self.delta_time)
        self.renderer.render(self.scene, self.camera)

Example(screen_size=[800, 600]).run()
