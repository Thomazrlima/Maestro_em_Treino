from geometry.geometry import Geometry


class customGeometry(Geometry):
    def __init__(self, width=1, height=1, depth=1, pos_d=[], uv_data=[]):
        super().__init__()
        # Each side consists of two triangles
        position_data = pos_d
        
        self.add_attribute("vec3", "vertexPosition", position_data)
        self.add_attribute("vec2", "vertexUV", uv_data)
        self.count_vertices()
