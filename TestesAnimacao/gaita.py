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
        
        corpo_geometry = customGeometry(1, 1, 1, my_obj_reader('corpo_gaita.obj'))
        corpo_material = SurfaceMaterial(property_dict={"useVertexColors": True})
        self.corpo_mesh = Mesh(corpo_geometry, corpo_material)

        tecido_geometry = customGeometry(1, 1, 1, my_obj_reader('tecido_gaita.obj'))
        tecido_material = SurfaceMaterial(property_dict={"useVertexColors": True})
        self.tecido_mesh = Mesh(tecido_geometry, tecido_material)

        self.rig = MovementRig()
        self.rig.add(self.corpo_mesh)
        self.rig.add(self.tecido_mesh)
        
        self.rig.set_position([0, 0.5, -0.5])
        self.scene.add(self.rig)
        self.scene.add(AxesHelper(axis_length=2))
        
        grid = GridHelper(size=20, grid_color=[1, 1, 1], center_color=[1, 1, 0])
        grid.rotate_x(-math.pi / 2)
        self.scene.add(grid)

        self.animation_active = False
        self.current_animation = None
        self.animation_start_time = 0
        self.animation_duration = 3.0
        self.animation_speed = 1.5
        
        self.animations = {
            'm': {'type': 'inflate'}
        }

    def start_animation(self, key):
        if key in self.animations:
            self.animation_active = True
            self.current_animation = key
            self.animation_start_time = self.time
            print("\n--- Starting inflation animation ---")

    def update_animation(self, delta_time):
        if not self.animation_active or not self.current_animation:
            return

        elapsed = (self.time - self.animation_start_time) * self.animation_speed
        
        if elapsed > self.animation_duration:
            self.animation_active = False
            self.tecido_mesh.set_scale([1.0, 1.0, 1.0])
            print("Animation completed - reset to original scale")
            return

        progress = elapsed / self.animation_duration
        
        scale_factor = 0.5 + 1.5 * abs(math.sin(progress * math.pi * 2))
        self.tecido_mesh.set_scale([scale_factor, scale_factor, scale_factor])
        print(f"Current scale: {scale_factor:.2f}")

    def update(self):
        self.rig.update(self.input, self.delta_time)

        if self.input.is_key_pressed('m') and not self.animation_active:
            self.start_animation('m')

        self.update_animation(self.delta_time)
        self.renderer.render(self.scene, self.camera)

Example(screen_size=[800, 600]).run()
