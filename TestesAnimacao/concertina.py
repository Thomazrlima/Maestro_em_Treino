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
from core.obj_reader_harmonica import my_obj_reader
from core_ext.object3d import Object3D
from geometry.harmonicGeometry import customGeometry 
from material.texture import TextureMaterial
from material.phong import PhongMaterial
from core_ext.texture import Texture

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
        self.rig.add(self.sanfonaver)
        self.rig.add(self.sanfonabra)
        self.rig.add(self.sanfonadir)
        self.rig.add(self.sanfonadirbra)
        self.rig.add(self.sanfonadirpreto)
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
        fole_texture = Texture(file_name="images/branco.jpg")
        fole_vertices, fole_uv = my_obj_reader('instrumentos/fole.obj')
        fole_array = np.array(fole_vertices)
        geometry = customGeometry(1, 1, 1, fole_array.tolist(), fole_uv)
        material = TextureMaterial(texture=fole_texture)
        self.fole = Mesh(geometry, material)
        self.fole.set_position([0, 0, 0])

        esq_vertices, esq_uvs = my_obj_reader('instrumentos/sanfonadir.obj')
        vermelho_texture = Texture(file_name="images/vermelho.jpg")
        branco_texture = Texture(file_name="images/branco1.jpg")
        escuro_texture = Texture(file_name="images/escuro.jpg")
        preto_texture = Texture(file_name="images/preto.jpg")
        esq_array = np.array(esq_vertices)
        indexs = list(range(0,5375))
        geometry1_vertices = np.array([esq_array[i] for i in indexs], dtype= np.float32)
        geometry1_uvs = np.array([esq_uvs[i] for i in indexs], dtype= np.float32)
        geometry1 = customGeometry(1, 1, 1, geometry1_vertices, geometry1_uvs)
        material1 = TextureMaterial(texture=vermelho_texture)
        indexs2 = list(range(5376,7800))
        geometry2_vertices = np.array([esq_array[i] for i in indexs2], dtype= np.float32)
        geometry2_uvs = np.array([esq_uvs[i] for i in indexs2], dtype= np.float32)
        geometry2 = customGeometry(1, 1, 1, geometry2_vertices, geometry2_uvs)
        material2 = TextureMaterial(texture=escuro_texture)
        indexs3 = list(range(7801,17280))
        geometry3_vertices = np.array([esq_array[i] for i in indexs3], dtype= np.float32)
        geometry3_uvs = np.array([esq_uvs[i] for i in indexs3], dtype= np.float32)
        geometry3 = customGeometry(1, 1, 1, geometry3_vertices, geometry3_uvs)
        material3 = TextureMaterial(texture=branco_texture)
        self.sanfonaesq = Mesh(geometry1, material1)
        self.sanfonaver = Mesh(geometry2, material2)
        self.sanfonabra = Mesh(geometry3, material3)
        self.sanfonaesq.set_position([0, 0, 0])
        self.sanfonaver.set_position([0, 0, 0])
        self.sanfonabra.set_position([0, 0, 0])

        dir_vertices, dir_uvs = my_obj_reader('instrumentos/sanfonaesq.obj')
        dir_array = np.array(dir_vertices)
        print(len(dir_uvs))
        #12876
        indexs = list(range(0,10400))
        geometry1_vertices = np.array([dir_array[i] for i in indexs], dtype= np.float32)
        geometry1_uvs = np.array([dir_uvs[i] for i in indexs], dtype= np.float32)
        geometry1 = customGeometry(1, 1, 1, geometry1_vertices, geometry1_uvs)
        material1 = TextureMaterial(texture=vermelho_texture)
        indexs2 = list(range(10401,11420))
        geometry2_vertices = np.array([dir_array[i] for i in indexs2], dtype= np.float32)
        geometry2_uvs = np.array([dir_uvs[i] for i in indexs2], dtype= np.float32)
        geometry2 = customGeometry(1, 1, 1, geometry2_vertices, geometry2_uvs)
        material2 = TextureMaterial(texture=preto_texture)
        indexs3 = list(range(11421,12876))
        geometry3_vertices = np.array([dir_array[i] for i in indexs3], dtype= np.float32)
        geometry3_uvs = np.array([dir_uvs[i] for i in indexs3], dtype= np.float32)
        geometry3 = customGeometry(1, 1, 1, geometry3_vertices, geometry3_uvs)
        material3 = TextureMaterial(texture=branco_texture)
        material = SurfaceMaterial(property_dict={"useVertexColors": True})
        self.sanfonadir = Mesh(geometry1, material1)
        self.sanfonadir.set_position([0, 0, 0])
        self.sanfonadirbra = Mesh(geometry2, material2)
        self.sanfonadirbra.set_position([0, 0, 0])
        self.sanfonadirpreto = Mesh(geometry3, material3)
        self.sanfonadirpreto.set_position([0, 0, 0])

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
        self.sanfonabra.set_position([-half_width/2, 0, 0])
        self.sanfonaver.set_position([-half_width/2, 0, 0])
        self.sanfonadir.set_position([half_width/2, 0, 0])
        self.sanfonadirbra.set_position([half_width/2, 0, 0])
        self.sanfonadirpreto.set_position([half_width/2, 0, 0])

        self.renderer.render(self.scene, self.camera)

ConcertinaAnimation(screen_size=[800, 600]).run()
