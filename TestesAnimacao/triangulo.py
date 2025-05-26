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
from core.obj_reader_harmonica import my_obj_reader
from material.texture import TextureMaterial
from core_ext.texture import Texture


from geometry.harmonicGeometry import customGeometry

class TriangleAnimation(Base):
    def initialize(self):
        print("Initializing triangle animation...")
        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspect_ratio=800/600)
        self.camera.set_position([0, 1, 5])

        self.load_objects()

        self.rig = MovementRig()
        self.rig.add(self.triangle)
        self.rig.add(self.fio)
        self.rig.add(self.drumstick_pega)
        self.rig.add(self.drumstick_tubo)
        self.rig.set_position([0, 0.5, 0])
        self.scene.add(self.rig)

        self.scene.add(AxesHelper(axis_length=2))
        grid = GridHelper(size=20, grid_color=[1, 1, 1], center_color=[1, 1, 0])
        grid.rotate_x(-math.pi/2)
        self.scene.add(grid)

        self.swing_angle = 0
        self.swing_speed = 0
        self.swing_damping = 0.97
        self.max_swing_angle = math.pi / 6

        self.drumstick_state = "ready"
        self.hit_time = 0
        self.drumstick_progress = 0

    def load_objects(self):
        v, uv = my_obj_reader('instrumentos/triangulo.obj')
        corpo_verts = np.array(v[:6516], dtype=np.float32)
        corpo_tx = np.array(uv[:6516], dtype=np.float32)
        fio_verts = np.array(v[6516:], dtype=np.float32)
        fio_tx = np.array(uv[6516:], dtype=np.float32)

        highest_y = np.max(fio_verts[:, 1])
        corpo_verts[:, 1] -= highest_y
        fio_verts[:, 1] -= highest_y

        geometry = customGeometry(pos_d=corpo_verts, uv_data=corpo_tx)
        material = TextureMaterial(texture=Texture("images/metal.jpg"))
        self.triangle = Mesh(geometry, material)
        self.triangle.set_position([0, 2, 0])

        geometry = customGeometry(pos_d=fio_verts, uv_data=fio_tx)
        material = TextureMaterial(texture=Texture("images/tecido.jpg"))
        self.fio = Mesh(geometry, material)
        self.fio.set_position([0, 2, 0])

        v, uv = my_obj_reader('instrumentos/baqueta.obj')
        tubo_bastao_verts = np.array(v[:372], dtype=np.float32)
        tubo_bastao_tx = np.array(uv[:372], dtype=np.float32)
        pega_bastao_verts = np.array(v[372:], dtype=np.float32)
        pega_bastao_tx = np.array(uv[372:], dtype=np.float32)

        geometry = customGeometry(pos_d=tubo_bastao_verts, uv_data=tubo_bastao_tx)
        material = TextureMaterial(texture=Texture("images/metal.jpg"))
        self.drumstick_tubo = Mesh(geometry, material)
        self.drumstick_tubo.set_position([1, 1, 0])
        self.drumstick_tubo_initial_position = [1, 1, 0]

        geometry = customGeometry(pos_d=pega_bastao_verts, uv_data=pega_bastao_tx)
        material = TextureMaterial(texture=Texture("images/madeira.jpg"))
        self.drumstick_pega = Mesh(geometry, material)
        self.drumstick_pega.set_position([1, 1, 0])
        self.drumstick_pega_initial_position = [1, 1, 0]

    def hit_triangle(self):
        self.drumstick_state = "moving_forward"
        self.hit_time = self.time
        self.drumstick_progress = 0
        print("Triangle hit initiated")

    def update_drumstick(self):
        if self.drumstick_state == "moving_forward":
            self.drumstick_progress = min(1.0, (self.time - self.hit_time) / 0.4)

            self.drumstick_tubo.set_position([
                1 - self.drumstick_progress * 0.8,
                1 - self.drumstick_progress * 0.4,
                0
            ])
            self.drumstick_tubo.set_rotation([0, 0, -self.drumstick_progress * math.pi / 4])

            self.drumstick_pega.set_position([
                1 - self.drumstick_progress * 0.8,
                1 - self.drumstick_progress * 0.4,
                0
            ])
            self.drumstick_pega.set_rotation([0, 0, -self.drumstick_progress * math.pi / 4])


            if self.drumstick_progress >= 1.0:
                self.drumstick_state = "moving_back"
                self.hit_time = self.time
                self.swing_speed = 0.04

        elif self.drumstick_state == "moving_back":
            self.drumstick_progress = min(1.0, (self.time - self.hit_time) / 0.4)

            self.drumstick_tubo.set_position([
                0.2 + self.drumstick_progress * 0.8,
                0.6 + self.drumstick_progress * 0.4,
                0
            ])
            self.drumstick_tubo.set_rotation([
                0,
                0,
                -math.pi / 4 + self.drumstick_progress * math.pi / 4
            ])
            self.drumstick_pega.set_position([
                0.2 + self.drumstick_progress * 0.8,
                0.6 + self.drumstick_progress * 0.4,
                0
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

    def update(self):
        self.rig.update(self.input, self.delta_time)

        if self.input.is_key_pressed('h'):
            self.hit_triangle()

        if self.drumstick_state != "ready":
            self.update_drumstick()
            self.update_swing()

        self.renderer.render(self.scene, self.camera)

TriangleAnimation(screen_size=[800, 600]).run()
