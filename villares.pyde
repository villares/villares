from line_geometry import Line, simple_intersect
from line_geometry import draw_poly, par_hatch


def setup():
    size(500, 500, P3D)
    a = Line(100, 100, 300, 300, 300, 100)
    a.plot()
    print(a.dist())
