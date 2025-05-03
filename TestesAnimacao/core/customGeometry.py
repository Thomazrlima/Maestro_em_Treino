from geometry.geometry import Geometry


class customGeometry(Geometry):
    def __init__(self, width=1, height=1, depth=1, pos_d=[]):
        super().__init__()
        # vertices
        
        # colors for faces in order:
        # x+, x-, y+, y-, z+, z-
        c1, c2 = [0.6, 0.2, 0.6], [0.5, 0, 0]
        c3, c4 = [1, 0.6471, 0], [0, 0.5, 0]
        c5, c6 = [0.5882, 0.2941, 0], [0, 0, 0.5]
        # texture coordinates
        t0, t1, t2, t3 = [0, 0], [1, 0], [0, 1], [1, 1]
        # Each side consists of two triangles
        position_data = pos_d
        color_data = [c1] * int(len(position_data)/6) + [c2] * int(len(position_data)/6) + [c3] * int(len(position_data)/6) \
                   + [c4] * int(len(position_data)/6) + [c5] * int(len(position_data)/6) + [c6] * int(len(position_data)/6)
        uv_data = [t0, t1, t3, t0, t3, t2] * 6
        self.add_attribute("vec3", "vertexPosition", position_data)
        self.add_attribute("vec3", "vertexColor", color_data)
        self.add_attribute("vec2", "vertexUV", uv_data)
        self.count_vertices()
