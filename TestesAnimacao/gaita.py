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
from core.obj_reader import my_obj_reader1
from core.customGeometry import customGeometry
from core_ext.object3d import Object3D
from light.ambient_light import AmbientLight
from light.directional import DirectionalLight
from material.lambert import LambertMaterial
from extras.sun_light import SunLightHelper
from extras.text_texture import TextTexture
from material.texture import TextureMaterial
from geometry.rectangle import RectangleGeometry
from core.matrix import Matrix
from geometry.sphere import SphereGeometry
from material.phong import PhongMaterial
from core_ext.audio import Audio
from core_ext.texture import Texture
from geometry.custom import CustomGeometry
from core.obj_reader_harmonica import my_obj_reader 
from menu import SCREEN_HEIGHT, SCREEN_WIDTH

import subprocess
import pygame
import sys

from score.score import Score, euclidean_rhythm, check_rhythm
class Example(Base):
    def initialize(self):
        print("Initializing program...")
        self.renderer = Renderer()
        self.scene = Scene()

        self.camera = Camera(aspect_ratio=800/600)
        #self.camera.set_position([0.5, 1, 5])
        self.camera.rotate_y(math.pi / 2)
        self.camera.rotate_x(-math.pi / 7)
        self.camera.set_position([27, 8, 0])

        self.init_map()

        x = 26
        y = 6
        z = 0
        angulo = 0

        tecido_vertices, tecido_uv = my_obj_reader('instrumentos/tecido_gaita.obj')
        tecido_uv = [[u * 5, v * 5] for u, v in tecido_uv]
        tecido_vertices_array = np.array(tecido_vertices)
        tecido_center = np.mean(tecido_vertices_array, axis=0)
        centered_tecido_vertices = (tecido_vertices_array - tecido_center).tolist()
        
        tecido_geometry = CustomGeometry(1, 1, 1, centered_tecido_vertices, tecido_uv)
        tecido_texture = Texture("images/bag_cloth.jpg")
        tecido_material = PhongMaterial(texture=tecido_texture, number_of_light_sources=2, use_shadow=True)
        self.tecido_mesh = Mesh(tecido_geometry, tecido_material)
        self.tecido_mesh.rotate_x(angulo)
        self.tecido_mesh.set_position([x, y, z])

        corpo_vertices, corpo_uv = my_obj_reader('instrumentos/corpo_gaita.obj')
        corpo_uv = [[u , v * 4] for u, v in corpo_uv]
        corpo_vertices_array = np.array(corpo_vertices)
        centered_corpo_vertices = (corpo_vertices_array - tecido_center).tolist()
        corpo_geometry = CustomGeometry(1, 1, 1, centered_corpo_vertices, corpo_uv)
        corpo_texture = Texture("images/dark_oak.jpg")
        corpo_material = PhongMaterial(texture=corpo_texture, number_of_light_sources=2, use_shadow=True)
        self.corpo_mesh = Mesh(corpo_geometry, corpo_material)
        self.corpo_mesh.rotate_x(angulo)
        self.corpo_mesh.set_position([x, y, z])

        tubo_inferior_vertices, tubo_inferior_uv = my_obj_reader('instrumentos/tubo_inferior.obj')
        tubo_vertices_array = np.array(tubo_inferior_vertices)
        centered_tubo_vertices = (tubo_vertices_array - tecido_center).tolist()
        tubo_inferior_geometry = CustomGeometry(1, 1, 1, centered_tubo_vertices, tubo_inferior_uv)
        tubo_inferior_texture = Texture("images/dark_oak.jpg")
        tubo_inferior_material = PhongMaterial(texture=tubo_inferior_texture, number_of_light_sources=2, use_shadow=True)
        self.tubo_inferior_mesh = Mesh(tubo_inferior_geometry, tubo_inferior_material)
        self.tubo_inferior_mesh.rotate_x(angulo)
        self.tubo_inferior_mesh.set_position([x, y, z])
        self.tubo_inferior_mesh.translate(0, -0.1, 0)
        
        self.tubo_inferior_rotation = 0
        self.max_pendulum_angle = math.pi / 64

        self.main_group = Object3D()
        self.main_group.add(self.corpo_mesh)
        self.main_group.add(self.tecido_mesh)
        self.main_group.add(self.tubo_inferior_mesh)
        
        self.rig = MovementRig()
        self.rig.add(self.main_group)
        self.rig.set_position([0, 0.5, -0.5])
        self.scene.add(self.rig)

        self.rig.disable_movement()

        # self.scene.add(AxesHelper(axis_length=2))
        # grid = GridHelper(size=20, grid_color=[1, 1, 1], center_color=[1, 1, 0])
        # grid.rotate_x(-math.pi / 2)
        # self.scene.add(grid)

        self.animation_active = False
        self.current_animation = None
        self.animation_start_time = 0
        self.animation_duration = 3.0
        self.animation_speed = 1.5
        
        self.tecido_mesh.set_scale([1.0, 1.0, 1.0])
        
        self.animations = {
            'm': {'type': 'inflate'}
        }

        self.audio = Audio()
        self.audio.load(
           name='blowQ',
           filepath='used_sounds/Gaita/A#4_31.wav'
        )
        self.audio.load(
           name='blowW',
           filepath='used_sounds/Gaita/A4_31.wav'
        )
        self.audio.load(
           name='blowE',
           filepath='used_sounds/Gaita/B4_31.wav'
        )
        self.audio.load(
           name='blowR',
           filepath='used_sounds/Gaita/C#5_31.wav'
        )
        self.audio.load(
           name='blowT',
           filepath='used_sounds/Gaita/C5_32.wav'
        )
        self.audio.load(
           name='blowY',
           filepath='used_sounds/Gaita/E5_32.wav'
        )
        self.audio.load(
           name='blowU',
           filepath='used_sounds/Gaita/F#5_31.wav'
        )
        self.audio.load(
           name='blowI',
           filepath='used_sounds/Gaita/G4_31.wav'
        )
        self.audio.set_master_volume(0.05)
        self.keys = ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i']

        self.score = Score()
        self.euclideano = euclidean_rhythm(4, 8)
        self.tresillo = euclidean_rhythm(3, 8)
        self.cinquillo  = euclidean_rhythm(5, 8)
        self.sequence_started = False
        self.sequence_start_time = 0.0
        self.sequence_last_checked_slot = 0
        self.keys_in_slot = False
        self.input_sequence = []

        self.label_texture = TextTexture(text=f" Score: {self.score.value} ",
                                         system_font_name="Comicsans MS",
                                         font_size=35, font_color=[255, 180, 0],
                                         image_width=600, image_height=128,
                                         align_horizontal=0.5, align_vertical=0.5,
                                         transparent=True)

        self.label_material = TextureMaterial(self.label_texture)
        self.label_geometry = RectangleGeometry(width=2, height=0.5)
        self.label_geometry.apply_matrix(Matrix.make_rotation_y(np.pi/2))  # Rotate to face -z
        self.label = Mesh(self.label_geometry, self.label_material)
        self.label.set_position([23.5, 7.8, 1.9])
        self.scene.add(self.label)

    def checkScore(self, input_sequence):
        if check_rhythm(input_sequence, self.euclideano) or check_rhythm(input_sequence, self.tresillo) or check_rhythm(input_sequence, self.cinquillo):
            self.score.increment()
            self.scene.remove(self.label)

            self.label_texture = TextTexture(text=f" Score: {self.score.value} ",
                                         system_font_name="Comicsans MS",
                                         font_size=35, font_color=[255, 180, 0],
                                         image_width=600, image_height=128,
                                         align_horizontal=0.5, align_vertical=0.5,
                                         transparent=True)
            self.label_material = TextureMaterial(self.label_texture)
            self.label = Mesh(self.label_geometry, self.label_material)
            self.label.set_position([23.5, 7.8, 1.9])
            self.scene.add(self.label)
            
        self.sequence_started = False
        self.sequence_last_checked_slot = 0
        self.keys_in_slot = False
        self.input_sequence = []

    def init_map(self):
        n = 0.5
        ambient_light = AmbientLight(color=[0.1 * n, 0.1 * n, 0.1 * n])
        self.scene.add(ambient_light)

        m = 1
        self.directional_light = DirectionalLight(color=[0.8 * m, 0.8 * m, 0.8 * m], direction=[-1, -1, -2])
        self.scene.add(self.directional_light)

        self.sun_light_helper = SunLightHelper(self.directional_light, size=9)
        self.sun_light_helper.set_position([70, 80, 30])

        # self.directional_light.set_position([30, 30, 30])
        # self.directional_light.set_direction([10, -1, -90])
        self.directional_light.set_position([70, 80, 30])
        self.directional_light.set_direction([-20, -50, -90])

        # self.directional_light.add(directional_light_helper)
        self.directional_light.add(self.sun_light_helper)

        self.renderer.enable_shadows(self.directional_light)

        # --------------------------------------------------------------CEU-------------------------------------------------------------

        sky_geometry = SphereGeometry(radius=250)
        sky_material = TextureMaterial(texture=Texture(file_name="images/sky.jpg"))
        sky = Mesh(sky_geometry, sky_material)
        sky.rotate_y(2 * math.pi / 5)
        self.scene.add(sky)

        # -----------------------------------------------------------ALCATRAO-----------------------------------------------------------
        vertices, tex_coords = my_obj_reader('mapa_objs/alcatrao.obj')

        repeat_factor = 5.0

        tex_coords = [[u * repeat_factor, v * repeat_factor] for u, v in tex_coords]

        alcatrao_geometry = CustomGeometry(pos_d=vertices, uv=tex_coords)

        alcatrao_material = LambertMaterial(
            texture=Texture("images/Rubber004_4K-JPG_Color.jpg"),
            number_of_light_sources=2,
            use_shadow=True
        )

        alcatrao = Mesh(alcatrao_geometry, alcatrao_material)

        self.scene.add(alcatrao)

        # -----------------------------------------------------------PASSEIO-----------------------------------------------------------
        vertices, tex_coords = my_obj_reader('mapa_objs/passeio.obj')

        repeat_factor = 30

        tex_coords = [[u * repeat_factor, v * repeat_factor] for u, v in tex_coords]

        passeio_geometry = CustomGeometry(pos_d=vertices, uv=tex_coords)

        passeio_material = LambertMaterial(
            texture=Texture("images/passeio.png"),
            number_of_light_sources=2,
            use_shadow=True
        )

        passeio = Mesh(passeio_geometry, passeio_material)

        self.scene.add(passeio)

        # -----------------------------------------------------------CALÇADA-----------------------------------------------------------

        vertices, tex_coords = my_obj_reader('mapa_objs/calcada1.obj')

        repeat_factor = 1

        tex_coords = [[u * repeat_factor, v * repeat_factor] for u, v in tex_coords]

        calcada1_geometry = CustomGeometry(pos_d=vertices, uv=tex_coords)

        calcada1_material = LambertMaterial(
            texture=Texture("images/calcada.jpg"),
            number_of_light_sources=2,
            use_shadow=True
        )

        calcada1 = Mesh(calcada1_geometry, calcada1_material)

        self.scene.add(calcada1)
        # -----------------------------------calçada2------------------------------------------
        vertices, tex_coords = my_obj_reader('mapa_objs/calcada2.obj')

        repeat_factor = 1

        tex_coords = [[u * repeat_factor, v * repeat_factor] for u, v in tex_coords]

        calcada2_geometry = CustomGeometry(pos_d=vertices, uv=tex_coords)

        calcada2_material = LambertMaterial(
            texture=Texture("images/calcada2.jpeg"),
            number_of_light_sources=2,
            use_shadow=True
        )

        calcada2 = Mesh(calcada2_geometry, calcada2_material)

        self.scene.add(calcada2)

        # -----------------------------------calçada3------------------------------------------
        vertices, tex_coords = my_obj_reader('mapa_objs/calcada3.obj')

        repeat_factor = 1

        tex_coords = [[u * repeat_factor, v * repeat_factor] for u, v in tex_coords]

        calcada3_geometry = CustomGeometry(pos_d=vertices, uv=tex_coords)

        calcada3_material = LambertMaterial(
            texture=Texture("images/calcada.jpg"),
            number_of_light_sources=2,
            use_shadow=True
        )

        calcada3 = Mesh(calcada3_geometry, calcada3_material)

        self.scene.add(calcada3)

        # -----------------------------------calçada4------------------------------------------
        vertices, tex_coords = my_obj_reader('mapa_objs/calcada4.obj')

        repeat_factor = 1

        tex_coords = [[u * repeat_factor, v * repeat_factor] for u, v in tex_coords]

        calcada4_geometry = CustomGeometry(pos_d=vertices, uv=tex_coords)

        calcada4_material = LambertMaterial(
            texture=Texture("images/calcada3.jpeg"),
            number_of_light_sources=2,
            use_shadow=True
        )

        calcada4 = Mesh(calcada4_geometry, calcada4_material)

        self.scene.add(calcada4)

        # -----------------------------------------------------------CERCA-----------------------------------------------------------

        vertices, tex_coords = my_obj_reader('mapa_objs/cerca.obj')

        repeat_factor = 1

        tex_coords = [[u * repeat_factor, v * repeat_factor] for u, v in tex_coords]

        cerca_geometry = CustomGeometry(pos_d=vertices, uv=tex_coords)

        cerca_material = PhongMaterial(
            texture=Texture("images/Metal029_4K-JPG_Color.jpg"),
            number_of_light_sources=2,
            use_shadow=True
        )

        cerca = Mesh(cerca_geometry, cerca_material)

        self.scene.add(cerca)

        # -----------------------------------------------------------FONTE-----------------------------------------------------------

        vertices, tex_coords = my_obj_reader('mapa_objs/fonte.obj')

        repeat_factor = 0.5

        tex_coords = [[u * repeat_factor, v * repeat_factor] for u, v in tex_coords]

        fonte_geometry = CustomGeometry(pos_d=vertices, uv=tex_coords)

        fonte_material = PhongMaterial(
            texture=Texture("images/stone.jpg"),
            number_of_light_sources=2,
            use_shadow=True
        )

        fonte = Mesh(fonte_geometry, fonte_material)

        self.scene.add(fonte)

        # -----------------------------------------------------------PALCO-----------------------------------------------------------

        vertices, tex_coords = my_obj_reader('mapa_objs/palco.obj')

        repeat_factor = 1

        tex_coords = [[u * repeat_factor, v * repeat_factor] for u, v in tex_coords]

        palco_geometry = CustomGeometry(pos_d=vertices, uv=tex_coords)

        palco_material = PhongMaterial(
            texture=Texture("images/fonte.jpg"),
            number_of_light_sources=2,
            use_shadow=True
        )

        palco = Mesh(palco_geometry, palco_material)

        self.scene.add(palco)

        # -----------------------------------------------------------Bancos-----------------------------------------------------------

        vertices, tex_coords = my_obj_reader('mapa_objs/bancos.obj')

        bancos_geometry = CustomGeometry(pos_d=vertices, uv=tex_coords)

        bancos_material = PhongMaterial(
            texture=Texture("images/madeira2.jpg"),
            number_of_light_sources=2,
            use_shadow=True
        )

        bancos = Mesh(bancos_geometry, bancos_material)

        self.scene.add(bancos)

        # -----------------------------------------------------------PREDIO_1-----------------------------------------------------------

        vertices, tex_coords = my_obj_reader('mapa_objs/predio1.obj')
        repeat_factor = 5

        tex_coords = [[u * repeat_factor, v / 3 * repeat_factor] for u, v in tex_coords]
        predio1_geometry = CustomGeometry(pos_d=vertices, uv=tex_coords)

        predio1_material = PhongMaterial(
            texture=Texture("images/predio1.jpeg"),
            number_of_light_sources=2,
            use_shadow=True
        )

        predio1 = Mesh(predio1_geometry, predio1_material)

        self.scene.add(predio1)

        # -----------------------------------------------------------PREDIO_2-----------------------------------------------------------

        vertices, tex_coords = my_obj_reader('mapa_objs/predio2.obj')
        repeat_factor = 3

        tex_coords = [[u * repeat_factor, v * repeat_factor] for u, v in tex_coords]
        predio2_geometry = CustomGeometry(pos_d=vertices, uv=tex_coords)

        predio2_material = PhongMaterial(
            texture=Texture("images/predio2.jpg"),
            number_of_light_sources=2,
            use_shadow=True
        )

        predio2 = Mesh(predio2_geometry, predio2_material)

        self.scene.add(predio2)

        # -----------------------------------------------------------PREDIO_3-----------------------------------------------------------

        vertices, tex_coords = my_obj_reader('mapa_objs/predio3.obj')
        repeat_factor = 2

        tex_coords = [[u * repeat_factor, v * repeat_factor] for u, v in tex_coords]
        predio3_geometry = CustomGeometry(pos_d=vertices, uv=tex_coords)

        predio3_material = PhongMaterial(
            texture=Texture("images/predio3.jpg"),
            number_of_light_sources=2,
            use_shadow=True
        )

        predio3 = Mesh(predio3_geometry, predio3_material)

        self.scene.add(predio3)

        # -----------------------------------------------------------PREDIO_4-----------------------------------------------------------

        vertices, tex_coords = my_obj_reader('mapa_objs/predio4.obj')
        repeat_factor = 8

        tex_coords = [[u * repeat_factor, v / 2.3 * repeat_factor] for u, v in tex_coords]
        predio4_geometry = CustomGeometry(pos_d=vertices, uv=tex_coords)

        predio4_material = PhongMaterial(
            texture=Texture("images/predio4.jpg"),
            number_of_light_sources=2,
            use_shadow=True
        )

        predio4 = Mesh(predio4_geometry, predio4_material)

        self.scene.add(predio4)

        # -----------------------------------------------------------PREDIO_5-----------------------------------------------------------

        vertices, tex_coords = my_obj_reader('mapa_objs/predio5.obj')
        repeat_factor = 8

        tex_coords = [[u * repeat_factor, v / 1.5 * repeat_factor] for u, v in tex_coords]
        predio5_geometry = CustomGeometry(pos_d=vertices, uv=tex_coords)

        predio5_material = PhongMaterial(
            texture=Texture("images/predio6.jpg"),
            number_of_light_sources=2,
            use_shadow=True
        )

        predio5 = Mesh(predio5_geometry, predio5_material)

        self.scene.add(predio5)

        # -----------------------------------------------------------PREDIO_6-----------------------------------------------------------

        vertices, tex_coords = my_obj_reader('mapa_objs/predio6.obj')
        repeat_factor = 4

        tex_coords = [[u * repeat_factor, v * repeat_factor] for u, v in tex_coords]
        predio4_geometry = CustomGeometry(pos_d=vertices, uv=tex_coords)

        predio4_material = PhongMaterial(
            texture=Texture("images/predio5.jpg"),
            number_of_light_sources=2,
            use_shadow=True
        )

        predio4 = Mesh(predio4_geometry, predio4_material)

        self.scene.add(predio4)

        # -----------------------------------------------------------PREDIO_7-----------------------------------------------------------

        vertices, tex_coords = my_obj_reader('mapa_objs/predio7.obj')
        repeat_factor = 8

        tex_coords = [[u * repeat_factor, v / 3 * repeat_factor] for u, v in tex_coords]
        predio_geometry = CustomGeometry(pos_d=vertices, uv=tex_coords)

        predio_material = PhongMaterial(
            texture=Texture("images/predio7.jpg"),
            number_of_light_sources=2,
            use_shadow=True
        )

        predio = Mesh(predio_geometry, predio_material)

        self.scene.add(predio)

        # -----------------------------------------------------------PREDIO_8-----------------------------------------------------------

        vertices, tex_coords = my_obj_reader('mapa_objs/predio8.obj')
        repeat_factor = 8

        tex_coords = [[u * repeat_factor, v / 2.3 * repeat_factor] for u, v in tex_coords]
        predio_geometry = CustomGeometry(pos_d=vertices, uv=tex_coords)

        predio_material = PhongMaterial(
            texture=Texture("images/predio8.jpg"),
            number_of_light_sources=2,
            use_shadow=True
        )

        predio = Mesh(predio_geometry, predio_material)

        self.scene.add(predio)

        # -----------------------------------------------------------PREDIO_9-----------------------------------------------------------

        vertices, tex_coords = my_obj_reader('mapa_objs/predio9.obj')
        repeat_factor = 12

        tex_coords = [[u * repeat_factor, v / 7 * repeat_factor] for u, v in tex_coords]
        predio_geometry = CustomGeometry(pos_d=vertices, uv=tex_coords)

        predio_material = PhongMaterial(
            texture=Texture("images/predio9.jpeg"),
            number_of_light_sources=2,
            use_shadow=True
        )

        predio = Mesh(predio_geometry, predio_material)

        self.scene.add(predio)

        # -----------------------------------------------------------PREDIO_10-----------------------------------------------------------

        vertices, tex_coords = my_obj_reader('mapa_objs/predio10.obj')
        repeat_factor = 8

        tex_coords = [[u * repeat_factor, v / 3 * repeat_factor] for u, v in tex_coords]
        predio_geometry = CustomGeometry(pos_d=vertices, uv=tex_coords)

        predio_material = PhongMaterial(
            texture=Texture("images/predio10.jpg"),
            number_of_light_sources=2,
            use_shadow=True
        )

        predio = Mesh(predio_geometry, predio_material)

        self.scene.add(predio)

        # -----------------------------------------------------------PREDIO_11-----------------------------------------------------------

        vertices, tex_coords = my_obj_reader('mapa_objs/predio11.obj')
        repeat_factor = 8

        tex_coords = [[u * repeat_factor, v / 3 * repeat_factor] for u, v in tex_coords]
        predio_geometry = CustomGeometry(pos_d=vertices, uv=tex_coords)

        predio_material = PhongMaterial(
            texture=Texture("images/predio7.jpg"),
            number_of_light_sources=2,
            use_shadow=True
        )

        predio = Mesh(predio_geometry, predio_material)

        self.scene.add(predio)

        # -----------------------------------------------------------PREDIO_12-----------------------------------------------------------

        vertices, tex_coords = my_obj_reader('mapa_objs/predio12.obj')
        repeat_factor = 8

        tex_coords = [[u * repeat_factor, v / 4 * repeat_factor] for u, v in tex_coords]
        predio_geometry = CustomGeometry(pos_d=vertices, uv=tex_coords)

        predio_material = PhongMaterial(
            texture=Texture("images/predio8.jpg"),
            number_of_light_sources=2,
            use_shadow=True
        )

        predio = Mesh(predio_geometry, predio_material)

        self.scene.add(predio)

        # -----------------------------------------------------------PREDIO_13-----------------------------------------------------------

        vertices, tex_coords = my_obj_reader('mapa_objs/predio13.obj')
        repeat_factor = 8

        tex_coords = [[u * repeat_factor, v / 2.3 * repeat_factor] for u, v in tex_coords]
        predio_geometry = CustomGeometry(pos_d=vertices, uv=tex_coords)

        predio_material = PhongMaterial(
            texture=Texture("images/predio4.jpg"),
            number_of_light_sources=2,
            use_shadow=True
        )

        predio = Mesh(predio_geometry, predio_material)

        self.scene.add(predio)

        # -----------------------------------------------------------PREDIO_14-----------------------------------------------------------

        vertices, tex_coords = my_obj_reader('mapa_objs/predio14.obj')
        repeat_factor = 8

        tex_coords = [[u * repeat_factor, v / 2.3 * repeat_factor] for u, v in tex_coords]
        predio_geometry = CustomGeometry(pos_d=vertices, uv=tex_coords)

        predio_material = PhongMaterial(
            texture=Texture("images/predio11.jpg"),
            number_of_light_sources=2,
            use_shadow=True
        )

        predio = Mesh(predio_geometry, predio_material)

        self.scene.add(predio)

        # -----------------------------------------------------------PREDIO_15-----------------------------------------------------------

        vertices, tex_coords = my_obj_reader('mapa_objs/predio15.obj')
        repeat_factor = 8

        tex_coords = [[u * repeat_factor, v / 2.3 * repeat_factor] for u, v in tex_coords]
        predio_geometry = CustomGeometry(pos_d=vertices, uv=tex_coords)

        predio_material = PhongMaterial(
            texture=Texture("images/predio4.jpg"),
            number_of_light_sources=2,
            use_shadow=True
        )

        predio = Mesh(predio_geometry, predio_material)

        self.scene.add(predio)

        # -----------------------------------------------------------LOJA-----------------------------------------------------------

        vertices, tex_coords = my_obj_reader('mapa_objs/loja.obj')
        repeat_factor = 8

        tex_coords = [[u / 1.66 * repeat_factor, v * repeat_factor] for u, v in tex_coords]
        loja_geometry = CustomGeometry(pos_d=vertices, uv=tex_coords)

        loja_material = PhongMaterial(
            texture=Texture("images/predio_loja.jpg"),
            number_of_light_sources=2,
            use_shadow=True
        )

        loja = Mesh(loja_geometry, loja_material)

        self.scene.add(loja)

        # -----------------------------------------------PESSOA1---------------------------------------
        vertices, tex_coords = my_obj_reader('mapa_objs/pessoa.obj')
        pessoa_geometry = CustomGeometry(pos_d=vertices, uv=tex_coords)
        pessoa_material = TextureMaterial(texture=Texture("images/pessoa_vermelho.jpeg"))
        pessoa = Mesh(pessoa_geometry, pessoa_material)
        pessoa.scale(4)
        pessoa.translate(0, 0.1, -0.1)
        self.scene.add(pessoa)

        # -----------------------------------------------PESSOA2---------------------------------------
        vertices, tex_coords = my_obj_reader('mapa_objs/pessoa.obj')
        pessoa_geometry = CustomGeometry(pos_d=vertices, uv=tex_coords)
        pessoa_material = TextureMaterial(texture=Texture("images/pessoa_amarelo.jpg"))
        pessoa = Mesh(pessoa_geometry, pessoa_material)
        pessoa.scale(4)
        pessoa.rotate_y(math.pi)
        pessoa.translate(0, 0.1, -0.7)
        self.scene.add(pessoa)

        # -----------------------------------------------PESSOA3---------------------------------------------

        vertices, tex_coords = my_obj_reader('mapa_objs/sit_Mam.obj')
        pessoa_geometry = CustomGeometry(pos_d=vertices, uv=tex_coords)

        pessoa_material = TextureMaterial(
            texture=Texture("images/pessoa_azul.jpg")
        )

        pessoa = Mesh(pessoa_geometry, pessoa_material)
        pessoa.scale(4)
        pessoa.rotate_y(math.pi - math.pi / 5)
        pessoa.translate(3, 0.1, -0.3)
        self.scene.add(pessoa)

        self.directional_light.set_position([30, 30, 30])
        self.directional_light.set_direction([10, -1, -90])
    def start_animation(self, key):
        if key in self.animations:
            self.animation_active = True
            self.current_animation = key
            self.animation_start_time = self.time
            print("\n--- Starting inflation animation ---")

    def smooth_movement(self, t):
        """Função para suavizar o movimento pendular"""
        return math.sin(t * math.pi * 2) * (1 - math.exp(-5 * t)) * math.exp(-0.5 * t)

    def update_animation(self, delta_time):
        if not self.animation_active or not self.current_animation:
            return

        elapsed = (self.time - self.animation_start_time) * self.animation_speed
        
        if elapsed > self.animation_duration:
            self.animation_active = False
            self.tecido_mesh.set_scale([1.0, 1.0, 1.0])
            self.tubo_inferior_rotation = 0
            self.tubo_inferior_mesh.set_rotation([0, 0, 0])
            print("Animation completed - reset to original state")
            return

        progress = elapsed / self.animation_duration
        
        pendulum_factor = self.smooth_movement(progress)
        
        scale_factor = 1.0 + 0.05 * math.sin(progress * math.pi * 2)
        
        self.tecido_mesh.set_scale([scale_factor, scale_factor, scale_factor])
        
        self.tubo_inferior_rotation = pendulum_factor * self.max_pendulum_angle
        self.tubo_inferior_mesh.set_rotation([0, 0, self.tubo_inferior_rotation])

    def update(self):
        self.rig.update(self.input, self.delta_time)

        if self.input.is_key_down('return') and not self.animation_active:
            print("Enter pressionado - voltando para o menu")

            pygame.quit()
            subprocess.run([sys.executable, "menu.py"])

        for key in self.keys:
            if self.input.is_key_pressed(key) and not self.animation_active:
                if not self.sequence_started:
                    self.sequence_started = True
                    self.sequence_start_time = self.time
                    self.sequence_last_checked_slot = 0
                    self.keys_in_slot = True
                    self.input_sequence = []
                    print("Sequência de ritmo iniciada")
                elif self.sequence_started and self.sequence_last_checked_slot <= 8:
                    self.keys_in_slot = True
                self.start_animation('m')
                if self.input.is_key_down('q'):
                    print("Key 'q' pressed")
                    self.audio.play('blowQ')
                if self.input.is_key_down('w'):
                    print("Key 'w' pressed")
                    self.audio.play('blowW')
                if self.input.is_key_down('e'):
                    print("Key 'e' pressed")
                    self.audio.play('blowE')
                if self.input.is_key_down('r'):
                    print("Key 'r' pressed")
                    self.audio.play('blowR')
                if self.input.is_key_down('t'):
                    print("Key 't' pressed")
                    self.audio.play('blowT')
                if self.input.is_key_down('y'):
                    print("Key 'y' pressed")
                    self.audio.play('blowY')
                if self.input.is_key_down('u'):
                    print("Key 'u' pressed")
                    self.audio.play('blowU')
                if self.input.is_key_down('i'):
                    print("Key 'i' pressed")
                    self.audio.play('blowI')

            elif self.input.is_key_pressed(key) and self.animation_active:
                if self.input.is_key_down('q'):
                    print("Key 'q' pressed")
                    self.audio.play('blowQ')
                if self.input.is_key_down('w'):
                    print("Key 'w' pressed")
                    self.audio.play('blowW')
                if self.input.is_key_down('e'):
                    print("Key 'e' pressed")
                    self.audio.play('blowE')
                if self.input.is_key_down('r'):
                    print("Key 'r' pressed")
                    self.audio.play('blowR')
                if self.input.is_key_down('t'):
                    print("Key 't' pressed")
                    self.audio.play('blowT')
                if self.input.is_key_down('y'):
                    print("Key 'y' pressed")
                    self.audio.play('blowY')
                if self.input.is_key_down('u'):
                    print("Key 'u' pressed")
                    self.audio.play('blowU')
                if self.input.is_key_down('i'):
                    print("Key 'i' pressed")
                    self.audio.play('blowI')
        if self.sequence_started:
            elapsed = self.time - self.sequence_start_time
            current_slot = int(elapsed)
            if current_slot > self.sequence_last_checked_slot and current_slot <= 8:
                slot_val = 1 if self.keys_in_slot else 0
                self.input_sequence.append(slot_val)
                print(f"Slot {self.sequence_last_checked_slot + 1} → {slot_val}")
                self.keys_in_slot = False
                self.sequence_last_checked_slot = current_slot
                if current_slot == 8:
                    self.checkScore(self.input_sequence)
        self.update_animation(self.delta_time)
        self.renderer.render(self.scene, self.camera)

Example(screen_size=[SCREEN_WIDTH, SCREEN_HEIGHT]).run()