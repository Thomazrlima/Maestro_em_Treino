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
from core_ext.object3d import Object3D

class ConcertinaAnimation(Base):
    def initialize(self):
        print("Initializing concertina animation...")
        self.renderer = Renderer()
        self.scene = Scene()

        self.camera = Camera(aspect_ratio=800/600)
        self.camera.set_position([0, 1.5, 5])
        
        self.load_concertina_objects()
        
        self.main_group = Object3D()
        self.main_group.add(self.sanfonadir)
        self.main_group.add(self.sanfonaesq)
        self.main_group.add(self.fole)
        
        self.rig = MovementRig()
        self.rig.add(self.main_group)
        self.rig.set_position([0, 0.5, 0])
        self.scene.add(self.rig)
        
        self.scene.add(AxesHelper(axis_length=2))
        grid = GridHelper(size=20, grid_color=[1, 1, 1], center_color=[1, 1, 0])
        grid.rotate_x(-math.pi / 2)
        self.scene.add(grid)

        self.animation_active = False
        self.animation_start_time = 0
        self.animation_duration = 2.0
        self.max_expansion = 2.0
        self.side_movement = 0.5

    def load_concertina_objects(self):
        temp_vertices = my_obj_reader('instrumentos/sanfonadir.obj')
        center = np.mean(np.array(temp_vertices), axis=0)
        
        sanfonadir_vertices = my_obj_reader('instrumentos/sanfonadir.obj')
        sanfonadir_centered = (np.array(sanfonadir_vertices) - center).tolist()
        geometry = customGeometry(1, 1, 1, sanfonadir_centered)
        material = SurfaceMaterial(property_dict={"useVertexColors": True})
        self.sanfonadir = Mesh(geometry, material)
        self.sanfonadir_initial_pos = [0.5, 0, 0]
        self.sanfonadir.set_position(self.sanfonadir_initial_pos)
        
        sanfonaesq_vertices = my_obj_reader('instrumentos/sanfonaesq.obj')
        sanfonaesq_centered = (np.array(sanfonaesq_vertices) - center).tolist()
        geometry = customGeometry(1, 1, 1, sanfonaesq_centered)
        material = SurfaceMaterial(property_dict={"useVertexColors": True})
        self.sanfonaesq = Mesh(geometry, material)
        self.sanfonaesq_initial_pos = [-0.5, 0, 0]
        self.sanfonaesq.set_position(self.sanfonaesq_initial_pos)
        
        fole_vertices = my_obj_reader('instrumentos/fole.obj')
        fole_centered = (np.array(fole_vertices) - center).tolist()
        geometry = customGeometry(1, 1, 1, fole_centered)
        material = SurfaceMaterial(property_dict={"useVertexColors": True, "doubleSide": True})
        self.fole = Mesh(geometry, material)
        self.fole.set_position([0, 0, 0])
        self.fole_initial_scale = 1.0

    def start_animation(self):
        self.animation_active = True
        self.animation_start_time = self.time
        print("\n--- Starting concertina animation ---")

    def update_animation(self, delta_time):
        if not self.animation_active:
            return

        elapsed = self.time - self.animation_start_time
        progress = elapsed / self.animation_duration
        
        if progress >= 1.0:
            progress = 1.0
            self.animation_active = False
            print("Animation completed - returned to original state")
        
        t = math.sin(progress * math.pi)
        
        current_expansion = 1.0 + (self.max_expansion - 1.0) * t
        current_movement = self.side_movement * t
        
        self.fole.set_scale([current_expansion, 1, 1])
        
        self.sanfonadir.set_position([
            self.sanfonadir_initial_pos[0] + current_movement,
            self.sanfonadir_initial_pos[1],
            self.sanfonadir_initial_pos[2]
        ])
        
        self.sanfonaesq.set_position([
            self.sanfonaesq_initial_pos[0] - current_movement,
            self.sanfonaesq_initial_pos[1],
            self.sanfonaesq_initial_pos[2]
        ])

    def update(self):
        self.rig.update(self.input, self.delta_time)

        if self.input.is_key_pressed('a') and not self.animation_active:
            self.start_animation()

        self.update_animation(self.delta_time)
        self.renderer.render(self.scene, self.camera)

ConcertinaAnimation(screen_size=[800, 600]).run()
