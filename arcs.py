# -*- coding: utf-8 -*-

from line_geometry import intersecting, triangle_area

ROTATION = {0: 0,
            BOTTOM: 0,
            DOWN: 0,
            1: HALF_PI,
            LEFT: HALF_PI,
            2: PI,
            TOP: PI,
            UP: PI,
            3: PI + HALF_PI,
            RIGHT: PI + HALF_PI,
            BOTTOM + RIGHT: 0,
            DOWN + RIGHT: 0,
            DOWN + LEFT: HALF_PI,
            BOTTOM + LEFT: HALF_PI,
            TOP + LEFT: PI,
            UP + LEFT: PI,
            TOP + RIGHT: PI + HALF_PI,
            UP + RIGHT: PI + HALF_PI,
            }

def quarter_circle(x, y, radius, quadrant):
    circle_arc(x, y, radius, ROTATION[quadrant], HALF_PI)

def half_circle(x, y, radius, quadrant):
    circle_arc(x, y, radius, ROTATION[quadrant], PI)

def circle_arc(x, y, radius, start_ang, sweep_ang):
    arc(x, y, radius * 2, radius * 2, start_ang, start_ang + sweep_ang)

def b_circle_arc(x, y, radius, start_ang, sweep_ang, mode=0):
    b_arc(x, y, radius * 2, radius * 2, start_ang, start_ang + sweep_ang,
          mode=mode)

def b_arc_naked(cx, cy, w, h, start_angle, end_angle):
    b_arc(cx, cy, w, h, start_angle, end_angle, mode = 2)

def b_arc(cx, cy, w, h, start_angle, end_angle, mode=0):
    """
    Draw a bezier approximation of an arc using the same
    signature as the original Processing arc().
    mode: 0 "normal" arc, using beginShape() and endShape()
          1 "middle" used in recursive call of smaller arcs
          2 "naked" like normal, but without beginShape() and
             endShape() for use inside a larger PShape.
    """
    theta = end_angle - start_angle
    # Compute raw Bezier coordinates.
    if mode != 1 or abs(theta) < HALF_PI:
        x0 = cos(theta / 2.0)
        y0 = sin(theta / 2.0)
        x3 = x0
        y3 = 0 - y0
        x1 = (4.0 - x0) / 3.0
        if y0 != 0:
            y1 = ((1.0 - x0) * (3.0 - x0)) / (3.0 * y0)  # y0 != 0...
        else:
            y1 = 0
        x2 = x1
        y2 = 0 - y1
        # Compute rotationally-offset Bezier coordinates, using:
        # x' = cos(angle) * x - sin(angle) * y
        # y' = sin(angle) * x + cos(angle) * y
        bezAng = start_angle + theta / 2.0
        cBezAng = cos(bezAng)
        sBezAng = sin(bezAng)
        rx0 = cBezAng * x0 - sBezAng * y0
        ry0 = sBezAng * x0 + cBezAng * y0
        rx1 = cBezAng * x1 - sBezAng * y1
        ry1 = sBezAng * x1 + cBezAng * y1
        rx2 = cBezAng * x2 - sBezAng * y2
        ry2 = sBezAng * x2 + cBezAng * y2
        rx3 = cBezAng * x3 - sBezAng * y3
        ry3 = sBezAng * x3 + cBezAng * y3
        # Compute scaled and translated Bezier coordinates.
        rx, ry = w / 2.0, h / 2.0
        px0 = cx + rx * rx0
        py0 = cy + ry * ry0
        px1 = cx + rx * rx1
        py1 = cy + ry * ry1
        px2 = cx + rx * rx2
        py2 = cy + ry * ry2
        px3 = cx + rx * rx3
        py3 = cy + ry * ry3
        # Debug points... comment this out!
        # stroke(0)
        # ellipse(px3, py3, 15, 15)
        # ellipse(px0, py0, 5, 5)
    # Drawing
    if mode == 0: # 'normal' arc (not 'middle' nor 'naked')
        beginShape()
    if mode != 1: # if not 'middle'
        vertex(px3, py3)
    if abs(theta) < HALF_PI:
        bezierVertex(px2, py2, px1, py1, px0, py0)
    else:
        # to avoid distortion, break into 2 smaller arcs
        b_arc(cx, cy, w, h, start_angle, end_angle - theta / 2.0, mode=1)
        b_arc(cx, cy, w, h, start_angle + theta / 2.0, end_angle, mode=1)
    if mode == 0: # end of a 'normal' arc
        endShape()

def p_circle_arc(x, y, radius, start_ang, sweep_ang, mode=0, num_points=None):
    p_arc(x, y, radius * 2, radius * 2, start_ang, start_ang + sweep_ang,
          mode=mode, num_points=num_points)
                                

def p_arc(cx, cy, w, h, start_angle, end_angle, mode=0,
         num_points=None, vertex_func=vertex):
    """
    A poly approximation of an arc
    using the same signature as the original Processing arc()
    mode: 0 "normal" arc, using beginShape() and endShape()
          2 "naked" like normal, but without beginShape() and endShape()
          for use inside a larger PShape
    """
    if not num_points:
        num_points = 24  
    # start_angle = start_angle if start_angle < end_angle else start_angle - TWO_PI
    sweep_angle = end_angle - start_angle  
    if mode == 0:
            beginShape()
    if sweep_angle < 0:
        start_angle, end_angle = end_angle, start_angle
        sweep_angle = -sweep_angle 
        angle = sweep_angle / int(num_points)
        a = end_angle
        while a >= start_angle:
                sx = cx + cos(a) * w / 2.
                sy = cy + sin(a) * h / 2.
                vertex_func(sx, sy)
                a -= angle   
    elif sweep_angle > 0:
        angle = sweep_angle / int(num_points)
        a = start_angle
        while a <= end_angle:
                sx = cx + cos(a) * w / 2.
                sy = cy + sin(a) * h / 2.
                vertex_func(sx, sy)
                a += angle
    else:
        sx = cx + cos(start_angle) * w / 2.
        sy = cy + sin(start_angle) * h / 2.
        vertex_func(sx, sy)
    if mode == 0:
        endShape()

        
def poly_rounded2(p_list, r_list, open_poly=False, arc_func=arc):
    """
    draws a 'filleted' polygon with variable radius
    dependent on roundedCorner()
    """
    if not open_poly:
        with pushStyle():
            noStroke()
            beginShape()
            for p0, p1 in zip(p_list, [p_list[-1]] + p_list[:-1]):
                m = (PVector(p0.x, p0.y) + PVector(p1.x, p1.y)) / 2
                vertex(m.x, m.y)
            endShape(CLOSE)
        for p0, p1, p2, r in zip(p_list,
                                [p_list[-1]] + p_list[:-1],
                                [p_list[-2]] + [p_list[-1]] + p_list[:-2],
                                [r_list[-1]] + r_list[:-1]
                                ):
            m1 = (PVector(p0.x, p0.y) + PVector(p1.x, p1.y)) / 2
            m2 = (PVector(p2.x, p2.y) + PVector(p1.x, p1.y)) / 2
            roundedCorner(p1, m1, m2, r, arc_func)
    else:
            for p0, p1, p2, r in zip(p_list[:-1],
                                [p_list[-1]] + p_list[:-2],
                                [p_list[-2]] + [p_list[-1]] + p_list[:-3],
                                [r_list[-1]] + r_list[:-2]
                                ):
                m1 = (PVector(p0.x, p0.y) + PVector(p1.x, p1.y)) / 2
                m2 = (PVector(p2.x, p2.y) + PVector(p1.x, p1.y)) / 2
                roundedCorner(p1, m1, m2, r, arc_func)
            

def roundedCorner(pc, p1, p2, r, arc_func):
    """
    Based on Stackoverflow C# rounded corner post 
    https://stackoverflow.com/questions/24771828/algorithm-for-creating-rounded-corners-in-a-polygon
    """
    
    def GetProportionPoint(pt, segment, L, dx, dy):
        factor = float(segment) / L if L != 0 else segment
        return PVector((pt.x - dx * factor), (pt.y - dy * factor))

    # Vector 1
    dx1 = pc.x - p1.x
    dy1 = pc.y - p1.y

    # Vector 2
    dx2 = pc.x - p2.x
    dy2 = pc.y - p2.y

    # Angle between vector 1 and vector 2 divided by 2
    angle = (atan2(dy1, dx1) - atan2(dy2, dx2)) / 2

    # The length of segment between angular point and the
    # points of intersection with the circle of a given radius
    tng = abs(tan(angle))
    segment = r / tng if tng != 0 else r

    # Check the segment
    length1 = sqrt(dx1 * dx1 + dy1 * dy1)
    length2 = sqrt(dx2 * dx2 + dy2 * dy2)

    min_len = min(length1, length2)

    if segment > min_len:
        segment = min_len
        max_r = min_len * abs(tan(angle))
    else:
        max_r = r

    # Points of intersection are calculated by the proportion between
    # length of vector and the length of the segment.
    p1Cross = GetProportionPoint(pc, segment, length1, dx1, dy1)
    p2Cross = GetProportionPoint(pc, segment, length2, dx2, dy2)

    # Calculation of the coordinates of the circle
    # center by the addition of angular vectors.
    dx = pc.x * 2 - p1Cross.x - p2Cross.x
    dy = pc.y * 2 - p1Cross.y - p2Cross.y

    L = sqrt(dx * dx + dy * dy)
    d = sqrt(segment * segment + max_r * max_r)

    circlePoint = GetProportionPoint(pc, d, L, dx, dy)

    # StartAngle and EndAngle of arc
    startAngle = atan2(p1Cross.y - circlePoint.y, p1Cross.x - circlePoint.x)
    endAngle = atan2(p2Cross.y - circlePoint.y, p2Cross.x - circlePoint.x)

    # Sweep angle
    sweepAngle = endAngle - startAngle

    # Some additional checks
    if sweepAngle < 0:
        startAngle, endAngle = endAngle, startAngle
        sweepAngle = -sweepAngle

    if sweepAngle > PI:
        startAngle, endAngle = endAngle, startAngle
        sweepAngle = TWO_PI - sweepAngle

    # Draw result using graphics
    # noStroke()
    with pushStyle():
        noStroke()
        beginShape()
        vertex(p1.x, p1.y)
        vertex(p1Cross.x, p1Cross.y)
        vertex(p2Cross.x, p2Cross.y)
        vertex(p2.x, p2.y)
        endShape(CLOSE)

    line(p1.x, p1.y, p1Cross.x, p1Cross.y)
    line(p2.x, p2.y, p2Cross.x, p2Cross.y)
    arc_func(circlePoint.x, circlePoint.y, 2 * max_r, 2 * max_r,
        startAngle, startAngle + sweepAngle)

  
def circ_circ_tangent(p1, p2, r1, r2):
    d = dist(p1[0], p1[1], p2[0], p2[1])
    ri = r1 - r2
    line_angle = atan2(p1[0] - p2[0], p2[1] - p1[1])
    if d - abs(ri) >= 0:
        theta = asin(ri / float(d))
        x1 = -cos(line_angle + theta) * r1
        y1 = -sin(line_angle + theta) * r1
        x2 = -cos(line_angle + theta) * r2
        y2 = -sin(line_angle + theta) * r2
        return (line_angle + theta,
                (p1[0] - x1, p1[1] - y1),
                (p2[0] - x2, p2[1] - y2))
    else:
        return (None,
                (p1[0], p1[1]),
                (p2[0], p2[1]))

                
def arc_augmented_poly(op_list,
                       or_list=None,
                       check_intersection=False,
                       bezier_mode=True):
    """
    2020-09-22 Renamed from b_poly_arc_augmented 
    """
    
    if not op_list:
        return
    if or_list == None:
        r2_list = [0] * len(op_list)
    else:
        r2_list = or_list[:]
    assert len(op_list) == len(r2_list), \
        "Number of points and radii not the same"

    if check_intersection:
        bezier_mode = False
        global pontos_, vertex_func
        pontos_ = []
        vertex_func = lambda x, y: pontos_.append((x, y))
    else:
        vertex_func = vertex
    # remove overlapping adjacent points
    p_list, r_list = [], []
    for i1, p1 in enumerate(op_list):
        i2 = (i1 - 1)
        p2, r2, r1 = op_list[i2], r2_list[i2], r2_list[i1]
        if dist(p1[0], p1[1], p2[0], p2[1]) > 1:  # or p1 != p2:
            p_list.append(p1)
            r_list.append(r1)
        else:
            r2_list[i2] = min(r1, r2)
    # invert radius
    for i1, p1 in enumerate(p_list):
        i0 = (i1 - 1)
        p0 = p_list[i0]
        i2 = (i1 + 1) % len(p_list)
        p2 = p_list[i2]
        a = triangle_area(p0, p1, p2) / 1000.
        if or_list == None:
            r_list[i1] = a
        else:
            # if abs(a) < 1:
            #     r_list[i1] = r_list[i1] * abs(a)
            if a < 0:
                r_list[i1] = -r_list[i1]
    # reduce radius that won't fit
    for i1, p1 in enumerate(p_list):
        i2 = (i1 + 1) % len(p_list)
        p2, r2, r1 = p_list[i2], r_list[i2], r_list[i1]
        r_list[i1], r_list[i2] = reduce_radius(p1, p2, r1, r2)
    # calculate the tangents
    a_list = []
    for i1, p1 in enumerate(p_list):
        i2 = (i1 + 1) % len(p_list)
        p2, r2, r1 = p_list[i2], r_list[i2], r_list[i1]
        cct = circ_circ_tangent(p1, p2, r1, r2)
        a_list.append(cct)
    # check intersection
    if check_intersection:
        pontos = []
        for ang, p1, p2 in a_list:
            pontos.append(p1)
            pontos.append(p2)
        if intersecting(pontos):
            return True
        # else:
        #     return False
    # draw
    beginShape()
    for i1, ia in enumerate(a_list):
        i2 = (i1 + 1) % len(a_list)
        p1, p2, r1, r2 = p_list[i1], p_list[i2], r_list[i1], r_list[i2]
        a1, p11, p12 = ia
        a2, p21, p22 = a_list[i2]
        # circle(p1[0], p1[1], 10)
        if a1 != None and a2 != None:
            start = a1 if a1 < a2 else a1 - TWO_PI
            if r2 <= 0:
                a2 = a2 - TWO_PI
            abs_angle = abs(a2 - start)
            if abs_angle > TWO_PI:
                if a2 < 0:
                    a2 += TWO_PI  # a2 = a2 + TWO_PI
                else:
                    a2 -= TWO_PI  # a2 = a2 - TWO_PI

            if abs(a2 - start) != TWO_PI:
                if bezier_mode:
                    b_arc(p2[0], p2[1], r2 * 2, r2 * 2, start, a2,
                          mode=2)
                else:
                    p_arc(p2[0], p2[1], r2 * 2, r2 * 2, start, a2,
                          mode=2, num_points=4)
            # textSize(32)
            # text(str(int(degrees(start - a2))), p2[0], p2[1])
        else:
            # when the the segment is smaller than the diference between
            # radius, circ_circ_tangent won't renturn the angle
            # ellipse(p2[0], p2[1], r2 * 2, r2 * 2) # debug
            if a1:
                vertex_func(p12[0], p12[1])
            if a2:
                vertex_func(p21[0], p21[1])
    endShape(CLOSE)

    if check_intersection:
        if intersecting(pontos_):
            return True
        else:
            return False

def reduce_radius(p1, p2, r1, r2):
    d = dist(p1[0], p1[1], p2[0], p2[1])
    ri = abs(r1 - r2)
    if d - ri <= 0:
        if abs(r1) > abs(r2):
            r1 = map(d, ri + 1, 0, r1, r2)
        else:
            r2 = map(d, ri + 1, 0, r2, r1)
    return(r1, r2)
