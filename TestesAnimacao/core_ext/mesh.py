import OpenGL.GL as GL
import numpy as np
from core_ext.object3d import Object3D

class Mesh(Object3D):
    def __init__(self, geometry, material):
        super().__init__()
        self._geometry = geometry
        self._material = material
        self._visible = True
        self._scale = np.array([1.0, 1.0, 1.0], dtype=np.float32)
        
        self._translation_matrix = np.identity(4, dtype=np.float32)
        self._rotation_matrix = np.identity(4, dtype=np.float32)
        
        self._vao_ref = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(self._vao_ref)
        for variable_name, attribute_object in geometry.attribute_dict.items():
            attribute_object.associate_variable(material.program_ref, variable_name)
        GL.glBindVertexArray(0)

    def set_scale(self, scale):
        """Define a escala e atualiza a matriz de modelo"""
        if isinstance(scale, (int, float)):
            self._scale = np.array([scale, scale, scale], dtype=np.float32)
        else:
            self._scale = np.array(scale[:3], dtype=np.float32)
        
        self._update_transform()

    def set_position(self, position):
        """Define a posição e atualiza a matriz de translação"""
        super().set_position(position)
        self._translation_matrix = np.array([
            [1, 0, 0, position[0]],
            [0, 1, 0, position[1]],
            [0, 0, 1, position[2]],
            [0, 0, 0, 1]
        ], dtype=np.float32)
        self._update_transform()

    def _update_transform(self):
        """Atualiza a matriz global combinando todas as transformações"""
        scale_matrix = np.identity(4, dtype=np.float32)
        for i in range(3):
            scale_matrix[i,i] = self._scale[i]
        
        transform_matrix = self._translation_matrix @ self._rotation_matrix @ scale_matrix
        
        self.set_transform_matrix(transform_matrix)

    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, value):
        self._visible = bool(value)

    @property
    def geometry(self):
        return self._geometry

    @property
    def material(self):
        return self._material

    @property
    def vao_ref(self):
        return self._vao_ref
    