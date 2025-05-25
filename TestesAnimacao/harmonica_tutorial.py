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
        self.camera.set_position([0.5, 1, 5])
        v, uv = my_obj_reader('instrumentos/harmonic.obj')

        self.rig = MovementRig()
        self.rig.set_position([0.5, 0.8, 3])
        self.rig.rotate_y(math.pi / 2)
        self.rig.disable_movement()

        sky_geometry = SphereGeometry(radius=50)
        sky_material = TextureMaterial(texture=Texture(file_name="images/tecido_fundo.jpg"),
                                       property_dict={"repeatUV": [50, 50]})
        sky = Mesh(sky_geometry, sky_material)
        self.scene.add(sky)
        ground_geometry = RectangleGeometry(width=100, height=100)
        ground_material = TextureMaterial(
            texture=Texture(file_name="images/chao_tutorial.jpg"),
            property_dict={"repeatUV": [10, 10]},
            # number_of_light_sources=2,
            # use_shadow=True
        )
        ground = Mesh(ground_geometry, ground_material)
        ground.rotate_x(-math.pi / 2)
        self.scene.add(ground)

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

        cima_peq = Mesh(cima_peq_geometry, cima_peq_material)
        sphere = Mesh(sphere_geometry, sphere_material)
        sphere2 = Mesh(sphere2_geometry, sphere2_material)
        baixo = Mesh(baixo_geometry, baixo_material)
        cima = Mesh(cima_geometry, cima_material)
        baixo_peq = Mesh(baixo_peq_geometry, baixo_peq_material)
        sphere2_baixo = Mesh(sphere2_baixo_geometry, sphere2_baixo_material)
        sphere_baixo = Mesh(sphere_baixo_geometry, sphere_baixo_material)
        main = Mesh(main_geometry, main_material)

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
        # self.scene.add(AxesHelper(axis_length=2))

        # grid = GridHelper(size=20, grid_color=[1, 1, 1], center_color=[1, 1, 0])
        # grid.rotate_x(-math.pi / 2)
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

        self.label_texture = TextTexture(text=" Press 'Q' to start the 1st animation",
                                         system_font_name="Comicsans MS",
                                         font_size=33, font_color=[200, 0, 200],
                                         image_width=600, image_height=128,
                                         align_horizontal=0.5, align_vertical=0.5,
                                         image_border_width=4,
                                         image_border_color=[255, 0, 0])

        self.label_material = TextureMaterial(self.label_texture)
        self.label_geometry = RectangleGeometry(width=2, height=0.5)
        self.label_geometry.apply_matrix(Matrix.make_rotation_y(3.14))  # Rotate to face -z
        self.label = Mesh(self.label_geometry, self.label_material)
        self.label.set_position([0.5, 1.5, 3])
        self.scene.add(self.label)

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

        self.audio.volume_to(1)

        self._label4_active = False
        self._label4_start_time = 0.0
        self._schedule_sequence = False
        self._schedule_sequence_time = 0.0

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

            if self.current_animation in ('q', 'w'):
                self.downtime = True
                self.past_time = self.time

            if self.current_animation == 'e':
                self._schedule_sequence = True
                self._schedule_sequence_time = self.time

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
            self.animation_start_position[0] + displacement[0],
            self.animation_start_position[1] + displacement[1],
            self.animation_start_position[2]
        ]

        self.rig.set_position(new_position)

    def update_label(self):
        self.label_texture_2 = TextTexture(text=" Good job!",
                                           system_font_name="Comicsans MS",
                                           font_size=33, font_color=[200, 0, 200],
                                           image_width=600, image_height=128,
                                           align_horizontal=0.5, align_vertical=0.5,
                                           image_border_width=4,
                                           image_border_color=[255, 0, 0])
        self.label_material_2 = TextureMaterial(self.label_texture_2)
        self.label = Mesh(self.label_geometry, self.label_material_2)
        self.label.set_position([0.5, 1.5, 3])
        self.scene.add(self.label)

    def start_label2(self):
        self.label_texture_3 = TextTexture(text=" Press 'W' to start the 2nd animation",
                                           system_font_name="Comicsans MS",
                                           font_size=33, font_color=[200, 0, 200],
                                           image_width=600, image_height=128,
                                           align_horizontal=0.5, align_vertical=0.5,
                                           image_border_width=4,
                                           image_border_color=[255, 0, 0])
        self.label_material_3 = TextureMaterial(self.label_texture_3)
        self.label = Mesh(self.label_geometry, self.label_material_3)
        self.label.set_position([0.5, 1.5, 3])
        self.scene.add(self.label)

    def start_label3(self):
        self.label_texture_3 = TextTexture(text=" Press 'E' to start the 3rd animation",
                                           system_font_name="Comicsans MS",
                                           font_size=33, font_color=[200, 0, 200],
                                           image_width=600, image_height=128,
                                           align_horizontal=0.5, align_vertical=0.5,
                                           image_border_width=4,
                                           image_border_color=[255, 0, 0])
        self.label_material_3 = TextureMaterial(self.label_texture_3)
        self.label = Mesh(self.label_geometry, self.label_material_3)
        self.label.set_position([0.5, 1.5, 3])
        self.scene.add(self.label)

    def start_label4(self):
        self.label_texture_4 = TextTexture(text=" Here's an example of a sequence",
                                           system_font_name="Comicsans MS",
                                           font_size=33, font_color=[200, 0, 200],
                                           image_width=600, image_height=128,
                                           align_horizontal=0.5, align_vertical=0.5,
                                           image_border_width=4,
                                           image_border_color=[255, 0, 0])
        self.label_material_4 = TextureMaterial(self.label_texture_4)
        self.label = Mesh(self.label_geometry, self.label_material_4)
        self.label.set_position([0.5, 1.5, 3])
        self.scene.add(self.label)

    def start_label5(self):
        self.label_texture_5 = TextTexture(text=" Now your turn: Press 'T', 'Y', 'U', 'I'",
                                           system_font_name="Comicsans MS",
                                           font_size=33, font_color=[200, 0, 200],
                                           image_width=600, image_height=128,
                                           align_horizontal=0.5, align_vertical=0.5,
                                           image_border_width=4,
                                           image_border_color=[255, 0, 0])
        self.label_material_5 = TextureMaterial(self.label_texture_5)
        self.label = Mesh(self.label_geometry, self.label_material_5)
        self.label.set_position([0.5, 1.5, 3])
        self.scene.add(self.label)

    def start_sequence(self):
        if self.sequence_played:
            print("Sequence already played, ignoring subsequent calls.")
            return
        notes = ['blowQ', 'blowW', 'blowE', 'blowR']
        delay = 1
        for i, note in enumerate(notes):
            threading.Timer(delay * i, lambda n=note: self.audio.play(n)).start()
        self.start_animation('r')
        self.sequence_played = True

    def update(self):
        if self.label:
            self.label.look_at(self.camera.global_position)
        for key in self.animations:
            if self.input.is_key_pressed(key) and not self.animation_active:
                if self.input.is_key_pressed('q'):
                    self.start_animation('q')
                    self.scene.remove(self.label)
                    self.audio.play('blowQ')
                    self.last_key_pressed = 'q'
                if self.input.is_key_pressed('w'):
                    self.start_animation('w')
                    self.scene.remove(self.label)
                    self.audio.play('blowW')
                    self.last_key_pressed = 'w'
                if self.input.is_key_pressed('e'):
                    self.start_animation('e')
                    self.scene.remove(self.label)
                    self.audio.play('blowE')
                    self.last_key_pressed = 'e'
                if self.input.is_key_down('t'):
                    self.audio.play('blowT')
                if self.input.is_key_down('y'):
                    self.audio.play('blowY')
                if self.input.is_key_down('u'):
                    self.audio.play('blowU')
                if self.input.is_key_down('i'):
                    self.start_animation('i')
                    self.audio.play('blowI')
            if self.downtime is not None:
                elapsed_down = self.time - self.past_time
                if elapsed_down > 3.0:
                    self.downtime = None
                    self.past_time = 0.0
                    if self.last_key_pressed == 'q':
                        self.start_label2()
                    if self.last_key_pressed == 'w':
                        self.start_label3()

        if self._schedule_sequence and (self.time - self._schedule_sequence_time) >= 3.0:
            self.start_label4()
            self.start_sequence()

            self._label4_active = True
            self._label4_start_time = self.time

            self._schedule_sequence = False

        if self._label4_active and (self.time - self._label4_start_time) >= 3.0:
            if hasattr(self, 'label') and self.label is not None:
                self.scene.remove(self.label)
            self.start_label5()
            self._label4_active = False

        self.update_animation(self.delta_time)
        self.renderer.render(self.scene, self.camera)


Example(screen_size=[800, 600]).run()