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
from core_ext.object3d import Object3D
from core.customGeometry import customGeometry

class ConcertinaAnimation(Base):
    def initialize(self):
        print("Initializing concertina animation...")
        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspect_ratio=800/600)
        self.camera.set_position([0, 1, 5])
        
        self.base_fole_half_width = 2
        
        self.load_objects()

        self.rig = MovementRig()
        self.rig.add(self.fole)
        self.rig.add(self.sanfonaesq)
        self.rig.add(self.sanfonadir)
        self.rig.set_position([0, 0, 0])
        self.scene.add(self.rig)

        self.scene.add(AxesHelper(axis_length=2))
        grid = GridHelper(size=20, grid_color=[1, 1, 1], center_color=[1, 1, 0])
        grid.rotate_x(-math.pi/2)
        self.scene.add(grid)

        self.animation_active = False
        self.animation_duration = 2.0
        self.animation_elapsed = 0.0
        self.max_scale = 2.8

    def load_objects(self):
        fole_vertices = my_obj_reader('instrumentos/fole.obj')
        fole_array = np.array(fole_vertices)
        geometry = customGeometry(1, 1, 1, fole_array.tolist())
        material = SurfaceMaterial(property_dict={"useVertexColors": True})
        self.fole = Mesh(geometry, material)
        self.fole.set_position([0, 0, 0])

        esq_vertices = my_obj_reader('instrumentos/sanfonadir.obj')
        esq_array = np.array(esq_vertices)
        geometry = customGeometry(1, 1, 1, esq_array.tolist())
        material = SurfaceMaterial(property_dict={"useVertexColors": True})
        self.sanfonaesq = Mesh(geometry, material)
        self.sanfonaesq.set_position([0, 0, 0])

        dir_vertices = my_obj_reader('instrumentos/sanfonaesq.obj')
        dir_array = np.array(dir_vertices)
        geometry = customGeometry(1, 1, 1, dir_array.tolist())
        material = SurfaceMaterial(property_dict={"useVertexColors": True})
        self.sanfonadir = Mesh(geometry, material)
        self.sanfonadir.set_position([0, 0, 0])

    def update(self):
        self.rig.update(self.input, self.delta_time)

        if not self.animation_active and self.input.is_key_pressed('m'):
            self.animation_active = True
            self.animation_elapsed = 0.0

        if self.animation_active:
            self.animation_elapsed += self.delta_time
            progress = self.animation_elapsed / self.animation_duration

            if progress <= 0.5:
                scale_x = 1.0 + (self.max_scale - 1.0) * (progress / 0.5)
                move_factor = (progress / 0.5)
                half_width = self.base_fole_half_width * move_factor
            elif progress <= 1.0:
                scale_x = self.max_scale - (self.max_scale - 1.0) * ((progress - 0.5) / 0.5)
                move_factor = 1 - ((progress - 0.5) / 0.5)
                half_width = self.base_fole_half_width * move_factor
            else:
                scale_x = 1.0
                half_width = 0.0
                self.animation_active = False
        else:
            scale_x = 1.0
            half_width = 0.0

        self.fole.set_scale([scale_x, 1, 1])
        self.sanfonaesq.set_position([-half_width/2, 0, 0])
        self.sanfonadir.set_position([half_width/2, 0, 0])

        self.renderer.render(self.scene, self.camera)

ConcertinaAnimation(screen_size=[800, 600]).run()
