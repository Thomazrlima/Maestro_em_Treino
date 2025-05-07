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
from extras.text_texture import TextTexture
from material.texture import TextureMaterial
from geometry.rectangle import RectangleGeometry
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
        
        self.rig.set_position([0.5, 0.8, 3])
        self.rig.rotate_y(math.pi / 2)
        self.rig.disable_movement()
        
        self.scene.add(self.rig)
        self.scene.add(AxesHelper(axis_length=2))
        
        grid = GridHelper(size=20, grid_color=[1, 1, 1], center_color=[1, 1, 0])
        grid.rotate_x(-math.pi / 2)
        self.scene.add(grid)

        self.animation_active = False
        self.animation_start_time = 0
        self.animation_duration = 4.0
        self.animation_speed = 2.5 
        self.animation_start_position = [0, 0, 0]
        self.movement_offsets = [0.4, -0.8, 0.4]

        self.label_texture = TextTexture(text=" Press 'X' to start animation",
                                    system_font_name="Comicsans MS",
                                    font_size=40, font_color=[200, 0, 200],
                                    image_width=600, image_height=128,
                                    align_horizontal=0.5, align_vertical=0.5,
                                    image_border_width=4,
                                    image_border_color=[255, 0, 0])

        self.label_material = TextureMaterial(self.label_texture)
        self.label_geometry = RectangleGeometry(width=2, height=0.5)
        self.label_geometry.apply_matrix(Matrix.make_rotation_y(3.14)) # Rotate to face -z
        self.label = Mesh(self.label_geometry, self.label_material)
        self.label.set_position([0.5, 1.5, 3])
        self.scene.add(self.label)

    def start_animation(self):
        self.animation_start_position = self.rig.get_position()
        self.animation_active = True
        self.animation_start_time = self.time
        print(f"Animation started from position: {self.animation_start_position}")

    def update_animation(self, delta_time):
        if not self.animation_active:
            return

        elapsed = (self.time - self.animation_start_time) * self.animation_speed
        
        if elapsed > self.animation_duration:
            self.animation_active = False
            self.rig.set_position(self.animation_start_position)
            print("Animation completed")
            self.update_label()
            return

        progress = elapsed / self.animation_duration
        
        if progress < 0.33:
            phase_progress = progress / 0.33
            movement = self.movement_offsets[0] * phase_progress
        elif progress < 0.66:
            phase_progress = (progress - 0.33) / 0.33
            movement = self.movement_offsets[0] + self.movement_offsets[1] * phase_progress
        else:
            phase_progress = (progress - 0.66) / 0.34
            movement = self.movement_offsets[0] + self.movement_offsets[1] + self.movement_offsets[2] * phase_progress
        
        new_position = [
            self.animation_start_position[0] + movement,
            self.animation_start_position[1],
            self.animation_start_position[2]
        ]

        self.rig.set_position(new_position)

    def update_label(self):
            self.label_texture_2 = TextTexture(text=" Good job!",
                                    system_font_name="Comicsans MS",
                                    font_size=40, font_color=[200, 0, 200],
                                    image_width=600, image_height=128,
                                    align_horizontal=0.5, align_vertical=0.5,
                                    image_border_width=4,
                                    image_border_color=[255, 0, 0])
            self.label_material_2 = TextureMaterial(self.label_texture_2)
            self.label = Mesh(self.label_geometry, self.label_material_2)
            self.label.set_position([0.5, 1.5, 3])
            self.scene.add(self.label)

    def update(self):
        self.rig.update(self.input, self.delta_time)
        if self.label:
            self.label.look_at(self.camera.global_position)
        self.label.look_at(self.camera.global_position)
        self.renderer.render(self.scene, self.camera)
        if self.input.is_key_down('x') and not self.animation_active:
            self.start_animation()
            self.scene.remove(self.label)
            
        if self.input.is_key_down('p'):
            print(f"Current position: {self.rig.get_position()}")
        self.update_animation(self.delta_time)

Example(screen_size=[800, 600]).run()
