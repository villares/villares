# from arcs import *

# def setup():
#     size(500, 500, P3D)
#     pontos = (50, 50),  (300, 400), (400, 50)
    
#     arc_augmented_poly(pontos, [30, 30, 30], auto_flip=True)


from villares.line_geometry import line_intersect, Line

def setup():
    size(500, 500)

def draw():
    background(230)
    path = (
        (50, 100),
        (250, 150),
        # (300, 450),
        (mouseX, mouseY),
        (450, 450),
    )
    with pushStyle():
        noFill()
        stroke(128)
        strokeWeight(5)
        beginShape()
        for x, y in path:
            vertex(x, y)
        endShape()
    offset = 20
    segments = []
    for (xa, ya), (xb, yb) in zip(path[:-1], path[1:]):
        angle = atan2(yb - ya, xb - xa)
        v = PVector.fromAngle(angle + HALF_PI) * offset 
        ro = (xa + v.x, ya + v.y, xb + v.x, yb + v.y)
        lo = (xa - v.x, ya - v.y, xb - v.x, yb - v.y)
        line(*ro)
        line(*lo)
        segments.append((xa, ya, xb, yb, ro, lo, angle))
        
    for sa, sb in zip(segments[:-1], segments[1:]):
        # angle_m = (sa[-1] + sb[-1]) / 2
        # v = PVector.fromAngle(angle_m + HALF_PI) * offset
        # xa, ya = sa[2:4]
        # line(xa - v.x, ya - v.y, xa + v.x, ya + v.y)
        roa = sa[4]
        rob = sb[4]
        p = line_intersect(Line(Line(*roa)), Line(*rob), in_segment=False)
        if p:
            circle(p[0], p[1], 5)
        loa = sa[5]
        lob = sb[5]
        p = line_intersect((loa[:2], loa[2:]), (lob[:2], lob[2:]), in_segment=False)
        if p:
            circle(p[0], p[1], 5)
