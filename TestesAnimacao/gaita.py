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

        tecido_vertices = my_obj_reader1('instrumentos/tecido_gaita.obj')
        tecido_vertices_array = np.array(tecido_vertices)
        tecido_center = np.mean(tecido_vertices_array, axis=0)
        centered_tecido_vertices = (tecido_vertices_array - tecido_center).tolist()
        
        tecido_geometry = customGeometry(1, 1, 1, centered_tecido_vertices)
        tecido_material = SurfaceMaterial(property_dict={"useVertexColors": True, "doubleSide": True})
        self.tecido_mesh = Mesh(tecido_geometry, tecido_material)
        self.tecido_mesh.rotate_x(angulo)
        self.tecido_mesh.set_position([x, y, z])

        corpo_vertices = my_obj_reader1('instrumentos/corpo_gaita.obj')
        corpo_vertices_array = np.array(corpo_vertices)
        centered_corpo_vertices = (corpo_vertices_array - tecido_center).tolist()
        corpo_geometry = customGeometry(1, 1, 1, centered_corpo_vertices)
        corpo_material = SurfaceMaterial(property_dict={"useVertexColors": True})
        self.corpo_mesh = Mesh(corpo_geometry, corpo_material)
        self.corpo_mesh.rotate_x(angulo)
        self.corpo_mesh.set_position([x, y, z])

        tubo_inferior_vertices = my_obj_reader1('instrumentos/tubo_inferior.obj')
        tubo_vertices_array = np.array(tubo_inferior_vertices)
        centered_tubo_vertices = (tubo_vertices_array - tecido_center).tolist()
        tubo_inferior_geometry = customGeometry(1, 1, 1, centered_tubo_vertices)
        tubo_inferior_material = SurfaceMaterial(property_dict={"useVertexColors": True})
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
        
        print(f"Current scale: {scale_factor:.3f}, Pendulum angle: {math.degrees(self.tubo_inferior_rotation):.1f}°")

    def update(self):
        self.rig.update(self.input, self.delta_time)

        if self.input.is_key_pressed('m') and not self.animation_active:
            self.start_animation('m')

        self.update_animation(self.delta_time)
        self.renderer.render(self.scene, self.camera)

Example(screen_size=[800, 600]).run()
