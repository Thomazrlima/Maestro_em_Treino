import math

from numpy.ma.core import repeat

from material.lambert import LambertMaterial
from extras.sun_light import SunLightHelper
from material.phong import PhongMaterial
from light.directional import DirectionalLight
from core.obj_reader_harmonica import my_obj_reader
from geometry.custom import CustomGeometry

from material.flat import FlatMaterial
from core.base import Base
from core_ext.camera import Camera
from core_ext.mesh import Mesh
from core_ext.renderer import Renderer
from core_ext.scene import Scene
from core_ext.texture import Texture
from geometry.rectangle import RectangleGeometry
from geometry.sphere import SphereGeometry
from material.texture import TextureMaterial
from extras.movement_rig import MovementRig
from light.ambient import AmbientLight
import random



class Example(Base):
    """
    Render a textured skysphere and a textured grass floor.
    Add camera movement: WASDRF(move), QE(turn), TG(look).
    """
    def initialize(self):
        print("Initializing program...")
        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspect_ratio=1700 / 1300)
        self.rig = MovementRig()
        self.rig.add(self.camera)
        self.scene.add(self.rig)
        self.rig.set_position([0, 5, 4])

        n = 0
        ambient_light = AmbientLight(color=[0.1 * n, 0.1 * n, 0.1 * n])
        self.scene.add(ambient_light)

        m = 1.5
        self.directional_light = DirectionalLight(color=[0.8 * m, 0.8 * m, 0.8 * m], direction=[-1, -1, -2])
        self.scene.add(self.directional_light)

        self.sun_light_helper = SunLightHelper(self.directional_light, size=9)
        self.sun_light_helper.set_position([0, 0, 11])

        self.directional_light.set_position([30, 30, 30])
        self.directional_light.set_direction([10, -50, -90])
        #self.directional_light.set_position([70, 80, -95])
        #self.directional_light.set_direction([0, -50, -90])

        # self.directional_light.add(directional_light_helper)
        self.directional_light.add(self.sun_light_helper)

        self.renderer.enable_shadows(self.directional_light)

        #--------------------------------------------------------------CEU-------------------------------------------------------------

        sky_geometry = SphereGeometry(radius=150)
        sky_material = TextureMaterial(texture=Texture(file_name="images/sky.jpg"))
        sky = Mesh(sky_geometry, sky_material)
        sky.rotate_y(2 * math.pi / 5)
        self.scene.add(sky)

        #-----------------------------------------------------------ALCATRAO-----------------------------------------------------------
        vertices, tex_coords = my_obj_reader('alcatrao.obj')

        repeat_factor = 5.0

        tex_coords = [[u * repeat_factor, v * repeat_factor] for u, v in tex_coords]

        alcatrao_geometry = CustomGeometry(pos_d=vertices, uv=tex_coords)

        alcatrao_material = LambertMaterial(
            texture=Texture("images/Rubber004_4K-JPG_Color.jpg"),
            number_of_light_sources=2,
            use_shadow= True
        )

        alcatrao = Mesh(alcatrao_geometry, alcatrao_material)

        self.scene.add(alcatrao)

        #-----------------------------------------------------------PASSEIO-----------------------------------------------------------
        vertices, tex_coords = my_obj_reader('passeio.obj')

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

        #-----------------------------------------------------------CALÇADA-----------------------------------------------------------

        vertices, tex_coords = my_obj_reader('calcada1.obj')

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
        #-----------------------------------calçada2------------------------------------------
        vertices, tex_coords = my_obj_reader('calcada2.obj')

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
        vertices, tex_coords = my_obj_reader('calcada3.obj')

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
        vertices, tex_coords = my_obj_reader('calcada4.obj')

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

        vertices, tex_coords = my_obj_reader('cerca.obj')

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

        vertices, tex_coords = my_obj_reader('fonte.obj')

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

        vertices, tex_coords = my_obj_reader('palco.obj')

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

        vertices, tex_coords = my_obj_reader('bancos.obj')

        bancos_geometry = CustomGeometry(pos_d=vertices, uv=tex_coords)

        bancos_material = PhongMaterial(
            texture=Texture("images/madeira2.jpg"),
            number_of_light_sources=2,
            use_shadow=True
        )

        bancos = Mesh(bancos_geometry, bancos_material)

        self.scene.add(bancos)

        # -----------------------------------------------------------PREDIO_1-----------------------------------------------------------

        vertices, tex_coords = my_obj_reader('predio1.obj')
        repeat_factor = 2

        tex_coords = [[u * repeat_factor, v * repeat_factor] for u, v in tex_coords]
        predio1_geometry = CustomGeometry(pos_d=vertices, uv=tex_coords)

        predio1_material = PhongMaterial(
            texture=Texture("images/predio1.jpeg"),
            number_of_light_sources=2,
            use_shadow=True
        )

        predio1 = Mesh(predio1_geometry, predio1_material)

        self.scene.add(predio1)

        # -----------------------------------------------------------PREDIO_2-----------------------------------------------------------

        vertices, tex_coords = my_obj_reader('predio2.obj')
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

        vertices, tex_coords = my_obj_reader('predio3.obj')
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


       # grass_geometry = RectangleGeometry(width=100, height=100)
       # grass_material = TextureMaterial(
       #     texture=Texture(file_name="images/grass.jpg"),
       #     property_dict={"repeatUV": [50, 50]}
       # )
       # grass = Mesh(grass_geometry, grass_material)
       # grass.rotate_x(-math.pi/2)
       # self.scene.add(grass)



    def update(self):
        self.rig.update(self.input, self.delta_time)
        self.renderer.render(self.scene, self.camera)


if __name__ == "__main__":
    Example(screen_size=[1700, 1300]).run()
