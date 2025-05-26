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
from core_ext.object3d import Object3D
from core.customGeometry import customGeometry
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

class TriangleAnimation(Base):
    def initialize(self):
        print("Initializing triangle animation...")
        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspect_ratio=800/600)
        self.camera.set_position([0, 1, 5])

        self.init_map()

        self.load_objects()

        self.rig = MovementRig()
        self.rig.add(self.triangle)
        self.rig.add(self.fio)
        self.rig.add(self.drumstick_pega)
        self.rig.add(self.drumstick_tubo)
        self.rig.rotate_y(math.pi/2)
        self.camera.rotate_y(math.pi / 2)
        self.camera.rotate_x(-math.pi / 7)
        self.camera.set_position([27, 8, 0])
        self.scene.add(self.rig)

        self.rig.disable_movement()

        # self.scene.add(AxesHelper(axis_length=2))
        # grid = GridHelper(size=20, grid_color=[1, 1, 1], center_color=[1, 1, 0])
        # grid.rotate_x(-math.pi/2)
        # self.scene.add(grid)

        self.swing_angle = 0
        self.swing_speed = 0
        self.swing_damping = 0.97
        self.max_swing_angle = math.pi / 6

        self.drumstick_state = "ready"
        self.hit_time = 0
        self.drumstick_progress = 0

    def load_objects(self):
        self.x = -2
        self.y = 7
        self.z = 24

        angulo = 0

        v, uv = my_obj_reader('instrumentos/triangulo.obj')
        corpo_verts = np.array(v[:6516], dtype=np.float32)
        corpo_tx = np.array(uv[:6516], dtype=np.float32)
        fio_verts = np.array(v[6516:], dtype=np.float32)
        fio_tx = np.array(uv[6516:], dtype=np.float32)

        highest_y = np.max(fio_verts[:, 1])
        corpo_verts[:, 1] -= highest_y
        fio_verts[:, 1] -= highest_y

        geometry = CustomGeometry(pos_d=corpo_verts, uv=corpo_tx)
        material = TextureMaterial(texture=Texture("images/metal.jpg"))
        self.triangle = Mesh(geometry, material)
        self.triangle.rotate_x(angulo)
        self.triangle.set_position([self.x, self.y, self.z])

        geometry = CustomGeometry(pos_d=fio_verts, uv=fio_tx)
        material = TextureMaterial(texture=Texture("images/tecido.jpg"))
        self.fio = Mesh(geometry, material)
        self.fio.set_position([self.x, self.y, self.z])

        v, uv = my_obj_reader('instrumentos/baqueta.obj')
        tubo_bastao_verts = np.array(v[:372], dtype=np.float32)
        tubo_bastao_tx = np.array(uv[:372], dtype=np.float32)
        pega_bastao_verts = np.array(v[372:], dtype=np.float32)
        pega_bastao_tx = np.array(uv[372:], dtype=np.float32)

        geometry = CustomGeometry(pos_d=tubo_bastao_verts, uv=tubo_bastao_tx)
        material = TextureMaterial(texture=Texture("images/metal.jpg"))
        self.drumstick_tubo = Mesh(geometry, material)
        self.drumstick_tubo.rotate_x(angulo)
        self.drumstick_tubo.set_position([self.x + 1, self.y - 1, self.z])
        self.drumstick_tubo_initial_position = [self.x + 1, self.y - 1, self.z]

        geometry = CustomGeometry(pos_d=pega_bastao_verts, uv=pega_bastao_tx)
        material = TextureMaterial(texture=Texture("images/madeira.jpg"))
        self.drumstick_pega = Mesh(geometry, material)
        self.drumstick_pega.set_position([self.x + 1, self.y - 1, self.z])
        self.drumstick_pega_initial_position = [self.x + 1, self.y - 1, self.z]


        #drumstick_vertices, drumstick_uvs = my_obj_reader('instrumentos/baqueta.obj')
        #drumstick_centered = np.array(drumstick_vertices)
        #geometry = customGeometry(1, 1, 1, drumstick_centered.tolist())
        #material = SurfaceMaterial(property_dict={"useVertexColors": True})
        #self.drumstick = Mesh(geometry, material)
        #self.drumstick.rotate_x(angulo)
        #self.drumstick.set_position([self.x+1, self.y-1, self.z])
        #self.drumstick_initial_position = [self.x+1, self.y-1, self.z]

    def hit_triangle(self):
        self.drumstick_state = "moving_forward"
        self.hit_time = self.time
        self.drumstick_progress = 0
        print("Triangle hit initiated")

    def update_drumstick(self):
        if self.drumstick_state == "moving_forward":
            self.drumstick_progress = min(1.0, (self.time - self.hit_time) / 0.4)

            #self.drumstick.set_position([
            #    self.drumstick_initial_position[0] - self.drumstick_progress * 0.8,
            #    self.drumstick_initial_position[1] - self.drumstick_progress * 0.4,
            #    self.drumstick_initial_position[2]
            #])
            #self.drumstick.set_rotation([0, 0, -self.drumstick_progress * math.pi / 4])

            self.drumstick_tubo.set_position([
                self.x + 1 - self.drumstick_progress * 0.8,
                self.y - 1 - self.drumstick_progress * 0.4,
                self.z
            ])
            self.drumstick_tubo.set_rotation([0, 0, -self.drumstick_progress * math.pi / 4])

            self.drumstick_pega.set_position([
                self.x + 1 - self.drumstick_progress * 0.8,
                self.y - 1 - self.drumstick_progress * 0.4,
                self.z
            ])
            self.drumstick_pega.set_rotation([0, 0, -self.drumstick_progress * math.pi / 4])

            if self.drumstick_progress >= 1.0:
                self.drumstick_state = "moving_back"
                self.hit_time = self.time
                self.swing_speed = 0.04

        elif self.drumstick_state == "moving_back":
            self.drumstick_progress = min(1.0, (self.time - self.hit_time) / 0.4)

            self.drumstick_tubo.set_position([
                self.x + 0.2 + self.drumstick_progress * 0.8,
                self.y - 0.9 + self.drumstick_progress * 0.4,
                self.z
            ])
            self.drumstick_tubo.set_rotation([
                0,
                0,
                -math.pi / 4 + self.drumstick_progress * math.pi / 4
            ])
            self.drumstick_pega.set_position([
                self.x + 0.2 + self.drumstick_progress * 0.8,
                self.y - 0.9 + self.drumstick_progress * 0.4,
                self.z
            ])
            self.drumstick_pega.set_rotation([
                0,
                0,
                -math.pi / 4 + self.drumstick_progress * math.pi / 4
            ])

            if self.drumstick_progress >= 1.0:
                self.drumstick_state = "swinging"
                self.drumstick_tubo.set_position(self.drumstick_tubo_initial_position)
                self.drumstick_tubo.set_rotation([0, 0, 0])
                self.drumstick_pega.set_position(self.drumstick_pega_initial_position)
                self.drumstick_pega.set_rotation([0, 0, 0])

    def update_swing(self):
        if self.drumstick_state in ["moving_back", "swinging"]:
            self.swing_angle -= self.swing_speed
            self.swing_speed *= self.swing_damping

            if abs(self.swing_angle) > self.max_swing_angle:
                self.swing_angle = self.max_swing_angle * np.sign(self.swing_angle)
                self.swing_speed *= -0.5

            if abs(self.swing_speed) < 0.001 and abs(self.swing_angle) < 0.01:
                self.swing_angle = self.swing_angle * 0.8

                if abs(self.swing_angle) < 0.001:
                    self.swing_angle = 0
                    self.drumstick_state = "ready"

            self.triangle.set_rotation([0, 0, self.swing_angle])
            self.fio.set_rotation([0, 0, self.swing_angle])
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
        self.rig.update(self.input, self.delta_time)

        if self.input.is_key_pressed('h'):
            self.hit_triangle()

        if self.drumstick_state != "ready":
            self.update_drumstick()
            self.update_swing()

        self.renderer.render(self.scene, self.camera)

TriangleAnimation(screen_size=[800, 600]).run()