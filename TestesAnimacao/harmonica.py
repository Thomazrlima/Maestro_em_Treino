import numpy as np
import math
import threading
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
from geometry.harmonicGeometry import customGeometry
from geometry.custom import CustomGeometry
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
class Example(Base):
    def initialize(self):
        print("Initializing program...")
        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspect_ratio=800 / 600)
        self.camera.rotate_y(math.pi / 2)
        self.camera.rotate_x(-math.pi / 6)
        self.camera.set_position([27, 8, 0])
        #self.rig2 = MovementRig()
        #self.rig2.add(self.camera)
        #self.scene.add(self.rig2)
        #self.rig2.set_position([0, 5, 4])
        v, uv = my_obj_reader('instrumentos/harmonic.obj')
        
        self.rig = MovementRig()
        self.rig.set_position([0.5, 0.8, 3])
        self.rig.rotate_y(math.pi)
        self.rig.rotate_z(-math.pi / 4)
        self.rig.disable_movement()


        self.init_map()

        cima_peq_index = list(range(0, 2748))
        sphere_index = list(range(2748, 5628))
        sphere2_index = list(range(5628, 8508))
        baixo_index = list(range(8508, 8820))
        cima_index = list(range(8820, 9132))
        baix_peq_index = list(range(9132, 11880))
        sphere2_baixo_index = list(range(11880, 14760))
        sphere_baixo_index = list(range(14760, 17640))
        main_index = list(range(17640, 22200))

        cima_peq_verts = np.array([v[i] for i in cima_peq_index], dtype=np.float32)
        cima_peq_tx = np.array([uv[i] for i in cima_peq_index], dtype=np.float32)
        sphere_verts = np.array([v[i] for i in sphere_index], dtype=np.float32)
        sphere_tx = np.array([uv[i] for i in sphere_index], dtype=np.float32)
        sphere2_verts = np.array([v[i] for i in sphere2_index], dtype=np.float32)
        sphere2_tx = np.array([uv[i] for i in sphere2_index], dtype=np.float32)
        baixo_verts = np.array([v[i] for i in baixo_index], dtype=np.float32)
        baixo_tx = np.array([uv[i] for i in baixo_index], dtype=np.float32)
        cima_verts = np.array([v[i] for i in cima_index], dtype=np.float32)
        cima_tx = np.array([uv[i] for i in cima_index], dtype=np.float32)
        baixo_peq_verts = np.array([v[i] for i in baix_peq_index], dtype=np.float32)
        baixo_peq_tx = np.array([uv[i] for i in baix_peq_index], dtype=np.float32)
        sphere2_baixo_verts = np.array([v[i] for i in sphere2_baixo_index], dtype=np.float32)
        sphere2_baixo_tx = np.array([uv[i] for i in sphere2_baixo_index], dtype=np.float32)
        sphere_baixo_verts = np.array([v[i] for i in sphere_baixo_index], dtype=np.float32)
        sphere_baixo_tx = np.array([uv[i] for i in sphere_baixo_index], dtype=np.float32)
        main_verts = np.array([v[i] for i in main_index], dtype=np.float32)
        main_tx = np.array([uv[i] for i in main_index], dtype=np.float32)

        cima_peq_geometry = customGeometry(pos_d=cima_peq_verts, uv_data=cima_peq_tx)
        sphere_geometry = customGeometry(pos_d=sphere_verts, uv_data=sphere_tx)
        sphere2_geometry = customGeometry(pos_d=sphere2_verts, uv_data=sphere2_tx)
        baixo_geometry = customGeometry(pos_d=baixo_verts, uv_data=baixo_tx)
        cima_geometry = customGeometry(pos_d=cima_verts, uv_data=cima_tx)
        baixo_peq_geometry = customGeometry(pos_d=baixo_peq_verts, uv_data=baixo_peq_tx)
        sphere2_baixo_geometry = customGeometry(pos_d=sphere2_baixo_verts, uv_data=sphere2_baixo_tx)
        sphere_baixo_geometry = customGeometry(pos_d=sphere_baixo_verts, uv_data=sphere_baixo_tx)
        main_geometry = customGeometry(pos_d=main_verts, uv_data=main_tx)

        cima_peq_texture = Texture(file_name="images/metal.jpg")
        sphere_texture = Texture(file_name="images/metal.jpg")
        sphere2_texture = Texture(file_name="images/metal.jpg")
        baixo_texture = Texture(file_name="images/madeira.jpg")
        cima_texture = Texture(file_name="images/madeira.jpg")
        baixo_peq_texture = Texture(file_name="images/metal.jpg")
        sphere2_baixo_texture = Texture(file_name="images/metal.jpg")
        sphere_baixo_texture = Texture(file_name="images/metal.jpg")
        main_texture = Texture(file_name="images/metal21.jpg")

        cima_peq_material = TextureMaterial(texture=cima_peq_texture)
        sphere_material = TextureMaterial(texture=sphere_texture)
        sphere2_material = TextureMaterial(texture=sphere2_texture)
        baixo_material = TextureMaterial(texture=baixo_texture)
        cima_material = TextureMaterial(texture=cima_texture)
        baixo_peq_material = TextureMaterial(texture=baixo_peq_texture)
        sphere2_baixo_material = TextureMaterial(texture=sphere2_baixo_texture)
        sphere_baixo_material = TextureMaterial(texture=sphere_baixo_texture)
        main_material = TextureMaterial(texture=main_texture, property_dict={"repeatUV": [7, 2]})
#        main_material = TextureMaterial(texture=main_texture)

        x = -22.1
        y = -13.3
        z = 3
        angulo = 0

        cima_peq = Mesh(cima_peq_geometry, cima_peq_material)
        cima_peq.rotate_x(angulo)
        cima_peq.set_position([x, y, z])
        #cima_peq.translate(x=x, y=y, z=z, local=False)

        sphere = Mesh(sphere_geometry, sphere_material)
        sphere.rotate_x(angulo)
        sphere.set_position([x, y, z])
        #sphere.translate(x=x, y=y, z=z, local=False)

        sphere2 = Mesh(sphere2_geometry, sphere2_material)
        sphere2.rotate_x(angulo)
        sphere2.set_position([x, y, z])
        #sphere2.translate(x=x, y=y, z=z, local=False)

        baixo = Mesh(baixo_geometry, baixo_material)
        baixo.rotate_x(angulo)
        baixo.set_position([x, y, z])
        #baixo.translate(x=x, y=y, z=z, local=False)

        cima = Mesh(cima_geometry, cima_material)
        cima.rotate_x(angulo)
        cima.set_position([x, y, z])
        #cima.translate(x=x, y=y, z=z, local=False)

        baixo_peq = Mesh(baixo_peq_geometry, baixo_peq_material)
        baixo_peq.rotate_x(angulo)
        baixo_peq.set_position([x, y, z])
        #baixo_peq.translate(x=x, y=y, z=z, local=False)

        sphere2_baixo = Mesh(sphere2_baixo_geometry, sphere2_baixo_material)
        sphere2_baixo.rotate_x(angulo)
        sphere2_baixo.set_position([x, y, z])
        #sphere2_baixo.translate(x=x, y=y, z=z, local=False)

        sphere_baixo = Mesh(sphere_baixo_geometry, sphere_baixo_material)
        sphere_baixo.rotate_x(angulo)
        sphere_baixo.set_position([x, y, z])
        #sphere_baixo.translate(x=x, y=y, z=z, local=False)

        main = Mesh(main_geometry, main_material)
        main.rotate_x(angulo)
        main.set_position([x, y, z])
        #main.translate(x=x, y=y, z=z, local=False)

        self.rig.add(cima_peq)
        self.rig.add(sphere)
        self.rig.add(sphere2)
        self.rig.add(baixo)
        self.rig.add(cima)
        self.rig.add(baixo_peq)
        self.rig.add(sphere2_baixo)
        self.rig.add(sphere_baixo)
        self.rig.add(main)
        
        self.scene.add(self.rig)
        #self.scene.add(AxesHelper(axis_length=2))
        
        #grid = GridHelper(size=20, grid_color=[1, 1, 1], center_color=[1, 1, 0])
        #grid.rotate_x(-math.pi / 2)
       # self.scene.add(grid)

        self.sequence_played = False

        self.animation_active = False
        self.current_animation = None
        self.downtime = None
        self.past_time = 0
        self.last_key_pressed = None
        self.animation_start_time = 0
        self.animation_duration = 1.0
        self.animation_speed = 1.0 
        self.animation_start_position = [0, 0.5, -0.5]
        
        self.animations = {
            'q': {'direction': [1.0, 0.0, 0.0], 'intensity': 1.0}, 
            'w': {'direction': [-1.0, 0.0, 0.0], 'intensity': 1.0},
            'e': {'direction': [1.0, 0.0, 0.0], 'intensity': 0.8, 'oscillate': True},
            'r': {'direction': [-1.0, 0.0, 0.0], 'intensity': 0.8, 'oscillate': True},
            't': {'direction': [-1.0, 0.1, 0.0], 'intensity': 0.8},
            'y': {'direction': [1.0, 0.05, 0.0], 'intensity': 1.2},
            'u': {'direction': [-1.0, 0.05, 0.0], 'intensity': 1.2},
            'i': {'direction': [1.0, 0.0, 0.0], 'intensity': 0.6},
            'o': {'direction': [-1.0, 0.0, 0.0], 'intensity': 0.6},
            'p': {'direction': [1.0, 0.05, 0.0], 'intensity': 0.8},
            '[': {'direction': [-1.0, 0.1, 0.0], 'intensity': 1.3}
        }

        self.audio = Audio()
        self.audio.load(
           name='blowQ',
           filepath='used_sounds/FitHarmonica/553291__sukondi__high-c-played-on-harmonica.mp3'
        )
        self.audio.load(
           name='blowW',
           filepath='used_sounds/FitHarmonica/553290__sukondi__high-d-played-on-harmonica.mp3'
        )
        self.audio.load(
           name='blowE',
           filepath='used_sounds/FitHarmonica/553289__sukondi__high-e-played-on-harmonica.mp3'
        )
        self.audio.load(
           name='blowR',
           filepath='used_sounds/FitHarmonica/553294__sukondi__high-f-played-on-harmonica.mp3'
        )
        self.audio.load(
           name='blowT',
           filepath='used_sounds/FitHarmonica/553293__sukondi__high-g-played-on-harmonica.mp3'
        )
        self.audio.load(
           name='blowY',
           filepath='used_sounds/FitHarmonica/553292__sukondi__high-a-played-on-harmonica.mp3'
        )
        self.audio.load(
           name='blowU',
           filepath='used_sounds/FitHarmonica/553295__sukondi__high-b-played-on-harmonica.mp3'
        )
        self.audio.load(
           name='blowI',
           filepath='used_sounds/FitHarmonica/DoMaior.mp3'
        )

        self.audio.set_master_volume(0.05)

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
        
        anim_params = self.animations[self.current_animation]
        direction = anim_params['direction']
        intensity = anim_params['intensity']
        
        if anim_params.get('oscillate', False):
            movement_progress = math.sin(progress * 2 * math.pi)
        else:
            movement_progress = math.sin(progress * math.pi)
        
        displacement = [
            direction[0] * intensity * movement_progress * 2,
            direction[1] * intensity * movement_progress * 2,
            0
        ]
        
        new_position = [
            self.animation_start_position[0] ,
            self.animation_start_position[1] + displacement[1],
            self.animation_start_position[2] + displacement[0]
        ]

        self.rig.set_position(new_position)

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

        self.directional_light.set_position([30, 30, 30])
        self.directional_light.set_direction([10, -1, -90])

    def update(self):
        self.audio.set_sound_volume('blowI', 2)
        for key in self.animations:
            if self.input.is_key_pressed(key) and not self.animation_active:
                if self.input.is_key_down('q'):
                    print("Key 'q' pressed")
                    self.start_animation('q')
                    self.audio.play('blowQ')
                if self.input.is_key_down('w'):
                    print("Key 'w' pressed")
                    self.start_animation('w')
                    self.audio.play('blowW')
                if self.input.is_key_down('e'):
                    print("Key 'e' pressed")
                    self.start_animation('e')
                    self.audio.play('blowE')
                if self.input.is_key_down('r'):
                    print("Key 'r' pressed")
                    self.start_animation('r')
                    self.audio.play('blowR')
                if self.input.is_key_down('t'):
                    print("Key 't' pressed")
                    self.start_animation('t')
                    self.audio.play('blowT')
                if self.input.is_key_down('y'):
                    print("Key 'y' pressed")
                    self.start_animation('y')
                    self.audio.play('blowY')
                if self.input.is_key_down('u'):
                    print("Key 'u' pressed")
                    self.start_animation('u')
                    self.audio.play('blowU')
                if self.input.is_key_down('i'):
                    print("Key 'i' pressed")
                    self.start_animation('i')
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
                                    
        self.update_animation(self.delta_time)
        self.rig.update(self.input, self.delta_time)
        self.renderer.render(self.scene, self.camera)


Example(screen_size=[800, 600]).run()
