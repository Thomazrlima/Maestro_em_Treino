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

class ConcertinaAnimation(Base):
    def initialize(self):
        print("Initializing concertina animation...")
        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspect_ratio=800/600)
        self.camera.rotate_y(math.pi / 2)
        self.camera.rotate_x(-math.pi / 7)
        self.camera.set_position([27, 8, 0])

        self.base_fole_half_width = 2

        self.init_map()

        x = 0
        y = 5.5
        z = 25
        angulo = 0

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
        self.sanfonaesq.rotate_x(angulo)

        self.sanfonaver = Mesh(customGeometry(1, 1, 1,
                                              esq_v[5376:7801].tolist(),
                                              esq_uv[5376:7801].tolist()), escuro)
        self.sanfonaver.rotate_x(angulo)

        self.sanfonabra = Mesh(customGeometry(1, 1, 1,
                                              esq_v[7802:17280].tolist(),
                                              esq_uv[7802:17280].tolist()), branco1)
        self.sanfonabra.rotate_x(angulo)


        #self.sanfonaesq.set_position([0, 0, 0])
        #self.sanfonaver.set_position([0, 0, 0])
        #self.sanfonabra.set_position([0, 0, 0])

        dir_v, dir_uv = my_obj_reader('instrumentos/sanfonaesq.obj')
        dir_v = np.array(dir_v, dtype=np.float32)
        dir_uv = np.array(dir_uv, dtype=np.float32)

        preto = TextureMaterial(Texture("images/preto.jpg"))
        #print(f"Número total de vértices em 'esq': {len(esq_v) // 3}")

        self.sanfonadir = Mesh(customGeometry(1, 1, 1,
                                              dir_v[0:3623].tolist(),
                                              dir_uv[0:3623].tolist()), vermelho)
        self.sanfonadir.rotate_x(angulo)
        
        self.sanfonadirbra = Mesh(customGeometry(1, 1, 1,
                                                 dir_v[3624:4400].tolist(),
                                                 dir_uv[3624:4400].tolist()), preto)
        self.sanfonadirbra.rotate_x(angulo)

        self.sanfonadirpreto = Mesh(customGeometry(1, 1, 1,
                                                   dir_v[4401:9164].tolist(),
                                                   dir_uv[4401:9164].tolist()), branco1)
        self.sanfonadirpreto.rotate_x(angulo)

        #self.sanfonadir.set_position([0, 0, 0])
        #self.sanfonadirbra.set_position([0, 0, 0])
       #self.sanfonadirpreto.set_position([0, 0, 0])

        self.rig = MovementRig()
        self.rig.rotate_y(math.pi / 2)
        self.rig.add(self.fole)
        self.rig.add(self.sanfonaesq)
        self.rig.add(self.sanfonaver)
        self.rig.add(self.sanfonabra)
        self.rig.add(self.sanfonadir)
        self.rig.add(self.sanfonadirbra)
        self.rig.add(self.sanfonadirpreto)
        #self.rig.set_position([0, 0, 0])
        self.scene.add(self.rig)

        self.rig.disable_movement()

        self.sanfonadirpreto.set_position([x, y, z])
        self.sanfonadirbra.set_position([x, y, z])
        self.sanfonadir.set_position([x, y, z])
        self.sanfonabra.set_position([x, y, z])
        self.sanfonaesq.set_position([x, y, z])
        self.sanfonaver.set_position([x, y, z])
        self.fole.set_position([x, y, z])

        # self.scene.add(AxesHelper(axis_length=2))
        # grid = GridHelper(size=20, grid_color=[1, 1, 1], center_color=[1, 1, 0])
        # grid.rotate_x(-math.pi / 2)
        # self.scene.add(grid)

        self.animation_active = False
        self.animation_duration = 2.0
        self.animation_elapsed = 0.0
        self.max_scale = 2.8

    def init_map(self):
        n = 0
        ambient_light = AmbientLight(color=[0.1 * n, 0.1 * n, 0.1 * n])
        self.scene.add(ambient_light)

        m = 1
        self.directional_light = DirectionalLight(color=[0.8 * m, 0.8 * m, 0.8 * m], direction=[-1, -1, -2])
        self.scene.add(self.directional_light)

        self.sun_light_helper = SunLightHelper(self.directional_light, size=9)
        self.sun_light_helper.set_position([0, 0, 11])

        # self.directional_light.set_position([30, 30, 30])
        # self.directional_light.set_direction([10, -1, -90])
        # self.directional_light.set_position([70, 80, -95])
        # self.directional_light.set_direction([0, -50, -90])

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
