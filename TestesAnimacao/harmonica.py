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
from core.obj_reader import my_obj_reader  
from core.customGeometry import customGeometry    
from extras.text_texture import TextTexture
from material.texture import TextureMaterial
from geometry.rectangle import RectangleGeometry
from core.matrix import Matrix

from core_ext.audio import Audio
class Example(Base):
    def initialize(self):
        print("Initializing program...")
        self.renderer = Renderer()
        self.scene = Scene()
        
        self.camera = Camera(aspect_ratio=800/600)
        self.camera.set_position([0.5, 1, 5])
        
        geometry = customGeometry(1, 1, 1, my_obj_reader('instrumentos/harmonic1.obj'))
        material = SurfaceMaterial(property_dict={"useVertexColors": True})
        self.mesh = Mesh(geometry, material)

        self.rig = MovementRig()
        self.rig.add(self.mesh)
        
        self.rig.set_position([0.5, 0.8, 3])
        self.rig.rotate_y(math.pi / 2)
        self.rig.disable_movement()
        
        self.scene.add(self.rig)
        self.scene.add(AxesHelper(axis_length=2))
        
        grid = GridHelper(size=20, grid_color=[1, 1, 1], center_color=[1, 1, 0])
        grid.rotate_x(-math.pi / 2)
        self.scene.add(grid)

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
        self.label_geometry.apply_matrix(Matrix.make_rotation_y(3.14)) # Rotate to face -z
        self.label = Mesh(self.label_geometry, self.label_material)
        self.label.set_position([0.5, 1.5, 3])
        self.scene.add(self.label)

        self.audio = Audio()
        self.audio.load(
           name='blowQ',
           filepath='used_sounds/FitHarmonica/553289__sukondi__high-e-played-on-harmonica.mp3'
        )
        self.audio.load(
           name='blowW',
           filepath='used_sounds/FitHarmonica/553290__sukondi__high-d-played-on-harmonica.mp3'
        )
        self.audio.load(
           name='blowE',
           filepath='used_sounds/FitHarmonica/553291__sukondi__high-c-played-on-harmonica.mp3'
        )
        self.audio.load(
           name='blowR',
           filepath='used_sounds/FitHarmonica/553292__sukondi__high-a-played-on-harmonica.mp3'
        )
        self.audio.load(
           name='blowT',
           filepath='used_sounds/FitHarmonica/553293__sukondi__high-g-played-on-harmonica.mp3'
        )
        self.audio.load(
           name='blowY',
           filepath='used_sounds/FitHarmonica/553294__sukondi__high-f-played-on-harmonica.mp3'
        )
        self.audio.load(
           name='blowU',
           filepath='used_sounds/FitHarmonica/553295__sukondi__high-b-played-on-harmonica.mp3'
        )
        self.audio.load(
           name='blowI',
           filepath='used_sounds/FitHarmonica/DoMaior.mp3'
        )

        self.audio.volume_to(0.3)


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
            self.update_label()
            self.downtime = 0
            self.past_time = self.time
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
            direction[0] * intensity * movement_progress,
            direction[1] * intensity * movement_progress,
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

    def update(self):
        self.rig.update(self.input, self.delta_time)
        if self.label:
            self.label.look_at(self.camera.global_position)
        for key in self.animations:
            if self.input.is_key_pressed(key) and not self.animation_active:
                self.start_animation(key)
                if self.input.is_key_pressed('q'):
                    self.scene.remove(self.label)
                    self.audio.play('blowQ')
                    self.last_key_pressed = 'q'
                if self.input.is_key_pressed('w'):
                    self.scene.remove(self.label)
                    self.audio.play('blowW')
                    self.last_key_pressed = 'w'
                if self.input.is_key_pressed('e'):
                    self.scene.remove(self.label)
                    self.audio.play('blowE')
                    self.last_key_pressed = 'e'
            if self.downtime is not None:
                elapsed_down = self.time - self.past_time
                if elapsed_down > 3.0:
                    self.past_time = 0.0
                    self.downtime = None
                    if self.last_key_pressed == 'q':
                        self.start_label2()
                    if self.last_key_pressed == 'w':
                        self.start_label3()
                    if self.last_key_pressed == 'e':
                        self.quit()
        self.update_animation(self.delta_time)
        self.renderer.render(self.scene, self.camera)

Example(screen_size=[800, 600]).run()
