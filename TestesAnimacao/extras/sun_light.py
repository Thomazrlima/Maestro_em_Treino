from geometry.sphere import SphereGeometry
from material.surface import SurfaceMaterial
from core_ext.mesh import Mesh


class SunLightHelper(Mesh):
    def __init__(self, point_light, size=0.1, line_width=1):
        #color = point_light.color
        #color = [1, 0.76, 0.13]
        color = [1, 1, 0]
        geometry = SphereGeometry(
            radius=size,
            radius_segments=20,
            height_segments=20)
        material = SurfaceMaterial(
            property_dict={
                "baseColor": color,
                "wireframe": False,
                "doubleSide": False,
                "lineWidth": line_width,
            }
        )
        super().__init__(geometry, material)
