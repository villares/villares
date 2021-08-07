from line_geometry import Line, simple_intersect
from line_geometry import draw_poly, par_hatch


def setup():
    size(500, 500)
    frameRate(2)
    
def draw():
    background(200)
    
    points = [(random(width), random(height)) 
              for _ in range(4)]
    draw_poly(points)
    lines = par_hatch(points, 10, 0, 1, 2)
    for l in lines:
        l.draw()
