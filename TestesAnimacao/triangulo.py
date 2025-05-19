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
from core_ext.object3d import Object3D
from core.customGeometry import customGeometry

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
        self.rig.add(self.drumstick)
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
        triangle_vertices = my_obj_reader('instrumentos/triangulo.obj')
        triangle_array = np.array(triangle_vertices)
        highest_y = np.max(triangle_array[:, 1])
        triangle_top_aligned = triangle_array.copy()
        triangle_top_aligned[:, 1] -= highest_y

        geometry = customGeometry(1, 1, 1, triangle_top_aligned.tolist())
        material = SurfaceMaterial(property_dict={"useVertexColors": True})
        self.triangle = Mesh(geometry, material)
        self.triangle.set_position([0, 2, 0])

        drumstick_vertices = my_obj_reader('instrumentos/baqueta.obj')
        drumstick_centered = np.array(drumstick_vertices)
        geometry = customGeometry(1, 1, 1, drumstick_centered.tolist())
        material = SurfaceMaterial(property_dict={"useVertexColors": True})
        self.drumstick = Mesh(geometry, material)
        self.drumstick.set_position([1, 1, 0])
        self.drumstick_initial_position = [1, 1, 0]

    def hit_triangle(self):
        self.drumstick_state = "moving_forward"
        self.hit_time = self.time
        self.drumstick_progress = 0
        print("Triangle hit initiated")

    def update_drumstick(self):
        if self.drumstick_state == "moving_forward":
            self.drumstick_progress = min(1.0, (self.time - self.hit_time) / 0.4)

            self.drumstick.set_position([
                1 - self.drumstick_progress * 0.8,
                1 - self.drumstick_progress * 0.4,
                0
            ])
            self.drumstick.set_rotation([0, 0, -self.drumstick_progress * math.pi / 4])

            if self.drumstick_progress >= 1.0:
                self.drumstick_state = "moving_back"
                self.hit_time = self.time
                self.swing_speed = 0.04

        elif self.drumstick_state == "moving_back":
            self.drumstick_progress = min(1.0, (self.time - self.hit_time) / 0.4)

            self.drumstick.set_position([
                0.2 + self.drumstick_progress * 0.8,
                0.6 + self.drumstick_progress * 0.4,
                0
            ])
            self.drumstick.set_rotation([
                0,
                0,
                -math.pi / 4 + self.drumstick_progress * math.pi / 4
            ])

            if self.drumstick_progress >= 1.0:
                self.drumstick_state = "swinging"
                self.drumstick.set_position(self.drumstick_initial_position)
                self.drumstick.set_rotation([0, 0, 0])

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

    def update(self):
        self.rig.update(self.input, self.delta_time)

        if self.input.is_key_pressed('h'):
            self.hit_triangle()

        if self.drumstick_state != "ready":
            self.update_drumstick()
            self.update_swing()

        self.renderer.render(self.scene, self.camera)

TriangleAnimation(screen_size=[800, 600]).run()
