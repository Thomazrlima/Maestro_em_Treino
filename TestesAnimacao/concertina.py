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
        
        if not self.check_files():
            return
            
        try:
            self.load_objects()
        except Exception as e:
            print(f"Erro ao carregar objetos: {e}")
            return

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

    def check_files(self):
        """Verifica se todos os arquivos necessários existem"""
        required_files = [
            'images/branco.jpg',
            'images/vermelho.jpg',
            'images/branco1.jpg',
            'images/escuro.jpg',
            'images/preto.jpg',
            'instrumentos/fole.obj',
            'instrumentos/sanfonadir.obj',
            'instrumentos/sanfonaesq.obj'
        ]
        
        missing_files = []
        for file in required_files:
            if not os.path.exists(file):
                missing_files.append(file)
                
        if missing_files:
            print("ERRO: Arquivos não encontrados:")
            for file in missing_files:
                print(f"- {file}")
            return False
        return True

    def safe_load_obj(self, file_path):
        """Carrega um arquivo OBJ com tratamento de erros"""
        try:
            vertices, uv = my_obj_reader(file_path)
            if len(vertices) == 0:
                raise ValueError(f"Arquivo OBJ vazio ou inválido: {file_path}")
            return vertices, uv
        except Exception as e:
            print(f"Erro ao carregar {file_path}: {e}")
            raise

    def create_mesh_safe(self, vertices, uvs, texture_file, indices=None):
        """Cria uma malha com verificação de limites"""
        try:
            if indices is not None:
                vertices = np.array([vertices[i] for i in indices if i < len(vertices)], dtype=np.float32)
                uvs = np.array([uvs[i] for i in indices if i < len(uvs)], dtype=np.float32)
            else:
                vertices = np.array(vertices, dtype=np.float32)
                uvs = np.array(uvs, dtype=np.float32)
                
            geometry = customGeometry(1, 1, 1, vertices.tolist(), uvs)
            texture = Texture(file_name=texture_file)
            material = TextureMaterial(texture=texture)
            return Mesh(geometry, material)
        except Exception as e:
            print(f"Erro ao criar malha: {e}")
            raise

    def load_objects(self):

        fole_vertices, fole_uv = self.safe_load_obj('instrumentos/fole.obj')
        self.fole = self.create_mesh_safe(fole_vertices, fole_uv, "images/branco.jpg")
        self.fole.set_position([0, 0, 0])

        esq_vertices, esq_uvs = self.safe_load_obj('instrumentos/sanfonadir.obj')
        vermelho_texture = "images/vermelho.jpg"
        branco_texture = "images/branco1.jpg"
        escuro_texture = "images/escuro.jpg"
        
        total_vertices = len(esq_vertices)
        indexs = list(range(0, min(5375, total_vertices)))
        indexs2 = list(range(5376, min(7800, total_vertices)))
        indexs3 = list(range(7801, min(17280, total_vertices)))
        
        self.sanfonaesq = self.create_mesh_safe(esq_vertices, esq_uvs, vermelho_texture, indexs)
        self.sanfonaver = self.create_mesh_safe(esq_vertices, esq_uvs, escuro_texture, indexs2)
        self.sanfonabra = self.create_mesh_safe(esq_vertices, esq_uvs, branco_texture, indexs3)
        
        self.sanfonaesq.set_position([0, 0, 0])
        self.sanfonaver.set_position([0, 0, 0])
        self.sanfonabra.set_position([0, 0, 0])

        dir_vertices, dir_uvs = self.safe_load_obj('instrumentos/sanfonaesq.obj')
        preto_texture = "images/preto.jpg"
        
        total_vertices_dir = len(dir_vertices)
        print(f"Total de vértices no OBJ direito: {total_vertices_dir}")
        
        indexs_dir1 = list(range(0, min(10400, total_vertices_dir)))
        indexs_dir2 = list(range(10401, min(11420, total_vertices_dir)))
        indexs_dir3 = list(range(11421, min(12876, total_vertices_dir)))
        
        self.sanfonadir = self.create_mesh_safe(dir_vertices, dir_uvs, vermelho_texture, indexs_dir1)
        self.sanfonadirbra = self.create_mesh_safe(dir_vertices, dir_uvs, preto_texture, indexs_dir2)
        self.sanfonadirpreto = self.create_mesh_safe(dir_vertices, dir_uvs, branco_texture, indexs_dir3)
        
        self.sanfonadir.set_position([0, 0, 0])
        self.sanfonadirbra.set_position([0, 0, 0])
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