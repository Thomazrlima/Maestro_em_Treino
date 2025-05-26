import pygame
import math
from core_ext.object3d import Object3D


class MovementRig(Object3D):
    def __init__(self, units_per_second=1, degrees_per_second=60):
        super().__init__()
        self._look_attachment = Object3D()
        self.children_list = [self._look_attachment]
        self._look_attachment.parent = self
        self._units_per_second = units_per_second
        self._degrees_per_second = degrees_per_second
        self._mouse_sensitivity = 0.01
        self._current_pitch = 0
        self._current_yaw = 0
        self._target_height = 0
        self._current_height = 0

        # Limites de movimento
        self.MIN_X = -33
        self.MAX_X = 33
        self.MIN_Z = -33
        self.MAX_Z = 33

        self.KEY_MOVE_FORWARDS = "w"
        self.KEY_MOVE_BACKWARDS = "s"
        self.KEY_MOVE_LEFT = "a"
        self.KEY_MOVE_RIGHT = "d"
        self.KEY_MOVE_UP = "r"
        self.KEY_MOVE_DOWN = "f"
        self.KEY_TURN_LEFT = "q"
        self.KEY_TURN_RIGHT = "e"
        self.KEY_LOOK_UP = "t"
        self.KEY_LOOK_DOWN = "g"
        self.KEY_SPRINT = "left shift"
        self.KEY_CROUCH = "left ctrl"
        self.KEY_JUMP = "space"
        self.KEY_RESTART_POSITION = "-"

        self.SPRINT_MULTIPLIER = 2.0
        self.CROUCH_FACTOR = 0.5
        self.CROUCH_HEIGHT = -2
        self.HEIGHT_SPEED = 3.0

        self.JUMP_HEIGHT = 3.0
        self.GRAVITY = 17.0
        self.jump_velocity = 0
        self.is_jumping = False
        self.is_grounded = True

    def disable_movement(self):
        self._movement_enabled = False

    def enable_movement(self):
        self._movement_enabled = True

    def get_position(self):
        """Returns the current position as a list [x, y, z]"""
        # The position is stored in the last column of the transformation matrix
        return list(self.local_matrix[0:3, 3])

    def add(self, child):
        self._look_attachment.add(child)

    def remove(self, child):
        self._look_attachment.remove(child)

    def _can_move(self, dx, dz):
        new_x = self.local_position[0] + dx
        new_z = self.local_position[2] + dz
        x_in_bounds = self.MIN_X <= new_x <= self.MAX_X
        z_in_bounds = self.MIN_Z <= new_z <= self.MAX_Z

        if not x_in_bounds or not z_in_bounds:
            return False

        return True

    def update(self, input_object, delta_time):
        move_amount = self._units_per_second * delta_time
        rotate_amount = self._degrees_per_second * (math.pi / 180) * delta_time

        sprint_active = input_object.is_key_pressed(self.KEY_SPRINT)
        crouching = input_object.is_key_pressed(self.KEY_CROUCH)
        speed_multiplier = 1.0
        if self._movement_enabled:
            if sprint_active and not crouching:
                speed_multiplier *= self.SPRINT_MULTIPLIER
            if crouching:
                speed_multiplier *= self.CROUCH_FACTOR

            if input_object.is_key_down(self.KEY_JUMP) and self.is_grounded and not crouching:
                self.is_jumping = True
                self.is_grounded = False
                self.jump_velocity = math.sqrt(2 * self.GRAVITY * self.JUMP_HEIGHT)

            if not self.is_grounded:
                self.jump_velocity -= self.GRAVITY * delta_time * 1.5
                height_change = self.jump_velocity * delta_time
                self._current_height += height_change

                if self._current_height <= 0:
                    self._current_height = 0
                    self.is_grounded = True
                    self.is_jumping = False
                    self.jump_velocity = 0

                self._look_attachment.translate(0, height_change, 0, local=False)

            if crouching and self.is_grounded:
                self._target_height = self.CROUCH_HEIGHT
                height_diff = self._target_height - self._current_height
                if abs(height_diff) > 0.01:
                    move = height_diff * self.HEIGHT_SPEED * delta_time
                    self._current_height += move
                    self._look_attachment.translate(0, move, 0, local=False)
            elif not crouching and self.is_grounded and not self.is_jumping:
                self._target_height = 0
                height_diff = self._target_height - self._current_height
                if abs(height_diff) > 0.01:
                    move = height_diff * self.HEIGHT_SPEED * delta_time
                    self._current_height += move
                    self._look_attachment.translate(0, move, 0, local=False)

            if input_object.is_key_pressed(self.KEY_MOVE_FORWARDS):
                if self._can_move(0, -move_amount * 7 * speed_multiplier):
                    self.translate(0, 0, -move_amount * 7 * speed_multiplier)
            if input_object.is_key_pressed(self.KEY_MOVE_BACKWARDS):
                if self._can_move(0, move_amount * 6 * speed_multiplier):
                    self.translate(0, 0, move_amount * 6 * speed_multiplier)
            if input_object.is_key_pressed(self.KEY_MOVE_LEFT):
                if self._can_move(-move_amount * 7 * speed_multiplier, 0):
                    self.translate(-move_amount * 7 * speed_multiplier, 0, 0)
            if input_object.is_key_pressed(self.KEY_MOVE_RIGHT):
                if self._can_move(move_amount * 7 * speed_multiplier, 0):
                    self.translate(move_amount * 7 * speed_multiplier, 0, 0)

            if input_object.mouse_captured:
                rel_x, rel_y = input_object.mouse_rel

                yaw_change = -rel_x * self._mouse_sensitivity
                pitch_change = -rel_y * self._mouse_sensitivity

                self.rotate_y(yaw_change, True)
                self._current_yaw += yaw_change

                new_pitch = self._current_pitch + pitch_change
                if abs(new_pitch) < math.pi / 2:
                    self._look_attachment.rotate_x(pitch_change, True)
                    self._current_pitch = new_pitch

                if pygame.display.get_init():
                    center = pygame.display.get_surface().get_rect().center
                    pygame.mouse.set_pos(center)
            else:
                if input_object.is_key_pressed(self.KEY_TURN_RIGHT):
                    self.rotate_y(-rotate_amount, True)
                if input_object.is_key_pressed(self.KEY_TURN_LEFT):
                    self.rotate_y(rotate_amount, True)
                if input_object.is_key_pressed(self.KEY_LOOK_UP):
                    self._look_attachment.rotate_x(-rotate_amount, True)
                if input_object.is_key_pressed(self.KEY_LOOK_DOWN):
                    self._look_attachment.rotate_x(rotate_amount, True)
