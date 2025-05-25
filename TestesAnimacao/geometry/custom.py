from OpenGL.GL import *
import numpy as np
from geometry.geometry import Geometry


class CustomGeometry(Geometry):
    def __init__(self, width=1, height=1, depth=1, pos_d=[], uv=[]):
        super().__init__()

        vertices = pos_d
        tex_coords = uv

        # Adiciona atributos
        uv2 = uv
        self.add_attribute("vec3", "vertexPosition", vertices)
        self.add_attribute("vec2", "vertexUV", tex_coords)
        self.count_vertices()

        # Remove o código desnecessário de cores (já que estamos usando texturas)