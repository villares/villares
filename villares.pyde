from arcs import arc_filleted_poly, arc_pts, arc_augmented_poly
from line_geometry import simplified_points

def setup():
    size(400, 400)
    # import arcs
    # arcs.DEBUG = True

def draw():
    background(200)
    input_points = ((100, 100),  (300, 200), (200, 300), (mouseX, mouseY))
    radii = [20, 50, 50, 20]
    strokeWeight(1)
    arc_augmented_poly(input_points, radii) #radius=50) 
    #arc_filleted_poly(input_points, radius=50) 
    strokeWeight(5)
    output_points = arc_augmented_poly(input_points,
                                      radii,
                                      #radius=50,
                                      arc_func=arc_pts,
                                      seg_len
                                      =5) 
    for x, y in simplified_points(output_points, 5):
        point(x, y)
