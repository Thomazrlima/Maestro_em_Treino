import numpy as np
import math
import os
from core.base import Base
from core_ext.camera import Camera
from core_ext.mesh import Mesh
from core_ext.renderer import Renderer
from core_ext.scene import Scene
from extras.axes import AxesHelper
from extras.grid import GridHelper
from extras.movement_rig import MovementRig
from material.texture import TextureMaterial
from core.obj_reader_harmonica import my_obj_reader
from geometry.harmonicGeometry import customGeometry
from core_ext.texture import Texture

class ConcertinaAnimation(Base):
    def initialize(self):
        print("Initializing concertina animation...")
        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspect_ratio=800/600)
        self.camera.set_position([0, 1, 5])

        self.base_fole_half_width = 2

        fole_v, fole_uv = my_obj_reader('instrumentos/fole.obj')
        fole_v = np.array(fole_v, dtype=np.float32)
        fole_uv = np.array(fole_uv, dtype=np.float32)

        fole_geometry = customGeometry(1, 1, 1, fole_v.tolist(), fole_uv.tolist())
        fole_texture = Texture(file_name="images/branco.jpg")
        fole_material = TextureMaterial(texture=fole_texture)
        self.fole = Mesh(fole_geometry, fole_material)
        self.fole.set_position([0, 0, 0])

        esq_v, esq_uv = my_obj_reader('instrumentos/sanfonadir.obj')
        esq_v = np.array(esq_v, dtype=np.float32)
        esq_uv = np.array(esq_uv, dtype=np.float32)

        vermelho = TextureMaterial(Texture("images/vermelho.jpg"))
        branco1 = TextureMaterial(Texture("images/branco1.jpg"))
        escuro = TextureMaterial(Texture("images/escuro.jpg"))

        self.sanfonaesq = Mesh(customGeometry(1, 1, 1,
                                              esq_v[0:5375].tolist(),
                                              esq_uv[0:5375].tolist()), vermelho)
        self.sanfonaver = Mesh(customGeometry(1, 1, 1,
                                              esq_v[5376:7801].tolist(),
                                              esq_uv[5376:7801].tolist()), escuro)
        self.sanfonabra = Mesh(customGeometry(1, 1, 1,
                                              esq_v[7802:17280].tolist(),
                                              esq_uv[7802:17280].tolist()), branco1)

        self.sanfonaesq.set_position([0, 0, 0])
        self.sanfonaver.set_position([0, 0, 0])
        self.sanfonabra.set_position([0, 0, 0])

        dir_v, dir_uv = my_obj_reader('instrumentos/sanfonaesq.obj')
        dir_v = np.array(dir_v, dtype=np.float32)
        dir_uv = np.array(dir_uv, dtype=np.float32)

        preto = TextureMaterial(Texture("images/preto.jpg"))
        print(f"Número total de vértices em 'esq': {len(esq_v) // 3}")

        self.sanfonadir = Mesh(customGeometry(1, 1, 1,
                                              dir_v[0:3623].tolist(),
                                              dir_uv[0:3623].tolist()), vermelho)
        self.sanfonadirbra = Mesh(customGeometry(1, 1, 1,
                                                 dir_v[3624:4400].tolist(),
                                                 dir_uv[3624:4400].tolist()), preto)
        self.sanfonadirpreto = Mesh(customGeometry(1, 1, 1,
                                                   dir_v[4401:9164].tolist(),
                                                   dir_uv[4401:9164].tolist()), branco1)

        self.sanfonadir.set_position([0, 0, 0])
        self.sanfonadirbra.set_position([0, 0, 0])
        self.sanfonadirpreto.set_position([0, 0, 0])

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
        grid.rotate_x(-math.pi / 2)
        self.scene.add(grid)

        self.animation_active = False
        self.animation_duration = 2.0
        self.animation_elapsed = 0.0
        self.max_scale = 2.8

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
        self.sanfonaesq.set_position([-half_width / 2, 0, 0])
        self.sanfonaver.set_position([-half_width / 2, 0, 0])
        self.sanfonabra.set_position([-half_width / 2, 0, 0])
        self.sanfonadir.set_position([half_width / 2, 0, 0])
        self.sanfonadirbra.set_position([half_width / 2, 0, 0])
        self.sanfonadirpreto.set_position([half_width / 2, 0, 0])

        self.renderer.render(self.scene, self.camera)

ConcertinaAnimation(screen_size=[800, 600]).run()
