# -*- coding: UTF-8 -*-
"""
From github.com/villares/villares/line_geometry.py

2020-09-25
2020-10-15 Fixed "line_instersection" typo, added dist() & removed TOLERANCE
2020-10-17 Added point_in_screen(), renamed poly() -> draw_poly()
2020-10-19 Fixed line_intersection typo, again :/, clean up, new point_inside_poly
2020-11-13 set of edges non-frozen option
2020-11-14 line_intersection now works with 2 tuples of 2 points, 4 points or 8 coords.
2020-11-20 Fixing Line that now accepts 1, 2 and 4 arguments; line_instance.draw() returns self
2020-11-20 New min_max algorithm (also adding bounding_box alias)
2020-11-20 rect_points(), rotate_point(), hatch_rect(), hatch_poly()
2020-11-22 Line .plot() method now accepts a custom drawing function. And so does hatch_poly().
2020-11-26 Line .plot() method to accept kwargs, added .as_PVector() as helper for Line objs.
2020-11-26 hatch_rect() fix
2020-12-03 min_max() fix for PVector (x, y z), replaced point_inside_poly & reverted som hatch_poly()
"""

from __future__ import division

class Line():

    def __init__(self, *args):
        if len(args) == 1:
            self.start = PVector(*args[0][0])
            self.end = PVector(*args[0][1])
        elif len(args) == 2:
            self.start = PVector(*args[0])
            self.end = PVector(*args[1])
        elif len(args) == 4:
            self.start = PVector(args[0], args[1])
            self.end = PVector(args[2], args[3])
        else:
            raise ValueError, "Requires 1 Line-like object, a pair of points, or x1, y1, x2, y2 coords."

    def __getitem__(self, i):
        return (self.start, self.end)[i]

    def dist(self):
        return PVector.dist(self.start, self.end)

    def plot(self, *args, **kwargs):
        function = kwargs.pop('function', None)
        ps = kwargs.get('ps', None)
        if not function and ps:
            ps.addChild(createShape(LINE,
                                    self[0][0], self[0][1],
                                    self[1][0], self[1][1]))
        elif not function:
            line(self[0][0], self[0][1], self[1][0], self[1][1])
        else:
            function(self[0][0], self[0][1], self[1][0], self[1][1],
                     *args, **kwargs)
        return self

    draw = plot

    def lerp(self, other, t):
        a = PVector.lerp(self.a, other.a, t)
        b = PVector.lerp(self.b, other.b, t)
        return Line(a, b)

    def line_point(self, t):
        return PVector.lerp(self[0], self[1], t)

    def midpoint(self):
        return PVector.lerp(self[0], self[1], 0.5)

    def intersect(self, other):
        return line_intersect(self, other)

    def contains_point(self, x, y, tolerance=0.1):
        return point_over_line(x, y,
                               self[0][0], self[0][1],
                               self[1][0], self[1][1],
                               tolerance)

    point_over = contains_point

    def as_PVector(self):
        return PVector(self[1][0], self[1][1]) - PVector(self[0][0], self[0][1])

    def point_colinear(self, x, y, tolerance=EPSILON):
        return points_are_colinear(x, y,
                                   self[0][0], self[0][1],
                                   self[1][0], self[1][1],
                                   tolerance)

def line_intersect(*args):
    """
    Adapted from Bernardo Fontes https://github.com/berinhard/sketches/
    2020-11-14 does not assume Line objects anymore, and works with 4 points or 8 coords.
    """
    if len(args) == 8:
        x1, y1, x2, y2, x3, y3, x4, y3 = args
        line_a = (x1, y1), (x2, y2)
        line_b = (x3, y3), (x4, y4)
    else:
        if len(args) == 2:
            line_a, line_b = args
        elif len(args) == 4:
            line_a = tuple(args[:2])
            line_b = tuple(args[2:])
        else:
            raise ValueError, "line_intersect requires 2 lines, 4 points or 8 coords."
        x1, y1 = line_a[0][0], line_a[0][1]
        x2, y2 = line_a[1][0], line_a[1][1]
        x3, y3 = line_b[0][0], line_b[0][1]
        x4, y4 = line_b[1][0], line_b[1][1]

    try:
        uA = ((x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)) / \
            ((y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1))
        uB = ((x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)) / \
            ((y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1))
    except ZeroDivisionError:
        return
    if not(0 <= uA <= 1 and 0 <= uB <= 1):
        return
    x = line_a[0][0] + uA * (line_a[1][0] - line_a[0][0])
    y = line_a[0][1] + uA * (line_a[1][1] - line_a[0][1])
    return PVector(x, y)

def point_over_line(px, py, lax, lay, lbx, lby,
                    tolerance=0.1):
    """
    Check if point is over line using the sum of
    the distances from the point to the line ends
    (the result has to be near equal for True).
    """
    ab = dist(lax, lay, lbx, lby)
    pa = dist(lax, lay, px, py)
    pb = dist(px, py, lbx, lby)
    return (pa + pb) <= ab + tolerance

def points_are_colinear(ax, ay, bx, by, cx, cy,
                        tolerance=EPSILON):
    """
    Test for colinearity by calculating the area
    of a triangle formed by the 3 points.
    """
    area = triangle_area((ax, ay), (bx, by), (cx, cy))
    return abs(area) < tolerance

def triangle_area(a, b, c):
    area = (a[0] * (b[1] - c[1]) +
            b[0] * (c[1] - a[1]) +
            c[0] * (a[1] - b[1]))
    return area

# class Poly():

#     def __init__(iterable):
#         self.__points = [p for p in iterable]

#     def __iter__(self):
#         return iter(self.__points)

#     def plot(self):
#         poly(self.__points)

#     draw = poly


def draw_poly(points, holes=None, closed=True):
    """
    Aceita como pontos sequencias de tuplas, lista ou vetores com (x, y) ou (x, y, z).
    Note que `holes` espera uma sequencias de sequencias ou uma única sequencia de
    pontos. Por default faz um polígono fechado.
    """

    def depth(seq):
        """
        usada para checar se temos um furo ou vários
        devolve 2 para um só furo, 3 para vários furos
        """
        if (isinstance(seq, list) or
                isinstance(seq, tuple) or
                isinstance(seq, PVector)):
            return 1 + max(depth(item) for item in seq)
        else:
            return 0

    beginShape()  # inicia o PShape
    for p in points:
        if len(p) == 2 or p[2] == 0:
            vertex(p[0], p[1])
        else:
            vertex(*p)  # desempacota pontos em 3d
    # tratamento dos furos, se houver
    holes = holes or []  # equivale a: holes if holes else []
    if holes and depth(holes) == 2:  # sequência única de pontos
        holes = (holes,)     # envolve em um tupla
    for hole in holes:  # para cada furo
        beginContour()  # inicia o furo
        for p in hole:
            if len(p) == 2 or p[2] == 0:
                vertex(p[0], p[1])
            else:
                vertex(*p)
        endContour()  # final e um furo
    # encerra o PShape
    if closed:
        endShape(CLOSE)
    else:
        endShape()

poly = draw_poly

def edges_as_sets(poly_points, frozen=True):
    """
    Return a (frozen)set of poly edges as frozensets of 2 points.
    """
    if frozen:
        return frozenset(frozenset(edge) for edge in poly_edges(poly_points))
    else:
        return set(frozenset(edge) for edge in poly_edges(poly_points))

def poly_edges(poly_points):
    """
    Return a list of edges (tuples containing pairs of points)
    for a list of points that represent a closed polygon
    """
    return pairwise(poly_points) + [(poly_points[-1], poly_points[0])]

edges = poly_edges

def pairwise(iterable):
    from itertools import tee
    "s -> (s0, s1), (s1, s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)

def min_max(points):
    """
    Return two PVectors with the most extreme coordinates,
    resulting in "bounding box" corners.
    """
    if len(points[0]) == 2:
        x_coordinates, y_coordinates = zip(*points)
        return (PVector(min(x_coordinates), min(y_coordinates)),
                PVector(max(x_coordinates), max(y_coordinates)))
    else:
        x_coordinates, y_coordinates, z_coordinates = zip(*points)
        return (PVector(min(x_coordinates), min(y_coordinates), min(z_coordinates)),
                PVector(max(x_coordinates), max(y_coordinates), max(z_coordinates)))

bounding_box = min_max

def par_hatch(points, divisions, *sides):
    vectors = [PVector(p[0], p[1]) for p in points]
    lines = []
    if not sides:
        sides = [0]
    for s in sides:
        a, b = vectors[-1 + s], vectors[+0 + s]
        d, c = vectors[-2 + s], vectors[-3 + s]
        for i in range(1, divisions):
            s0 = PVector.lerp(a, b, i / float(divisions))
            s1 = PVector.lerp(d, c, i / float(divisions))
            lines.append(Line(s0, s1))
    return lines

def is_poly_self_intersecting(poly_points):
    ed = edges(poly_points)
    intersect = False
    for a, b in ed[::-1]:
        for c, d in ed[2::]:
        # test only non consecutive edges
            if (a != c) and (b != c) and (a != d):
                if line_intersect(Line(a, b), Line(c, d)):
                    intersect = True
                    break
    return intersect

def point_inside_poly(x, y, points):
    # ray-casting algorithm based on
    # https://wrf.ecse.rpi.edu/Research/Short_Notes/pnpoly.html
    inside = False
    for i, p in enumerate(points):
        pp = points[i - 1]
        xi, yi = p
        xj, yj = pp
        intersect = ((yi > y) != (yj > y)) and (
            x < (xj - xi) * (y - yi) / (yj - yi) + xi)
        if intersect:
            inside = not inside
    return inside

def inter_lines(L, poly_points):
    inter_points = []
    for a, b in poly_edges(poly_points):
        inter = line_intersect(Line(a, b), L)
        if inter:
            inter_points.append(inter)
    if not inter_points:
        return []
    inter_lines = []
    if len(inter_points) > 1:
        inter_points.sort()
        pairs = zip(inter_points[::2], inter_points[1::2])
        for a, b in pairs:
            if a and b:
                inter_lines.append(Line(a, b))
    return inter_lines

def point_in_screen(p):
    return 0 <= p[0] <= width and 0 <= p[1] <= height

def hatch_poly(*args, **kwargs):
    if len(args) == 2:
        points, angle = args
        d = dist(points[0][0], points[0][1], points[2][0], points[2][1]) + EPSILON
        cx = (points[0][0] + points[1][0]) / 2.0
        cy = (points[1][1] + points[2][1]) / 2.0
    else:
        x, y, w, h, angle = args
        points = rect_points(x, y, w, h, kwargs.pop('mode', CORNER))
        bound = min_max(points)
        diag = Line(bound) 
        d = diag.dist() + EPSILON
        cx, cy, _ = diag.midpoint()
    spacing = kwargs.get('spacing', 5)
    function = kwargs.get('function', None)
    base = kwargs.pop('base', False)
    bound = min_max(points)
    diag = Line(bound)
    d = diag.dist()
    cx, cy, _ = diag.midpoint()
    num = int(d / spacing)
    rr = [rotate_point(x, y, angle, cx, cy)
          for x, y in rect_points(cx, cy, d, d, mode=CENTER)]
    # stroke(255, 0, 0)   # debug mode
    ab = Line(rr[0], rr[1])  # ;ab.plot()  # debug mode
    cd = Line(rr[3], rr[2])  # ;cd.plot()  # debug mode
    for i in range(num + 1):
        abp = ab.line_point(i / float(num) + EPSILON)
        cdp = cd.line_point(i / float(num) + EPSILON)
        if base == True:
            # add back base kwarg as a line
            kwargs['base_line'] = Line(abp, cdp)
        for hli in inter_lines(Line(abp, cdp), points):
            hli.plot(**kwargs)

def hatch_rect(*args, **kwargs):
    if len(args) == 2:
        r, angle = args
    else:
        x, y, w, h, angle = args
        r = rect_points(x, y, w, h, kwargs.get('mode', CORNER))
    spacing = kwargs.get('spacing', 10)
    function = kwargs.pop('function', None)
    base = kwargs.pop('base', False)
    d = dist(r[0][0], r[0][1], r[2][0], r[2][1])
    cx = (r[0][0] + r[1][0]) / 2.0
    cy = (r[1][1] + r[2][1]) / 2.0
    num = int(d / spacing)
    rr = [rotate_point(x, y, angle, cx, cy)
          for x, y in rect_points(cx, cy, d, d, mode=CENTER)]
    # stroke(255, 0, 0)   # debug mode
    ab = Line(rr[0], rr[1])  # ;ab.plot()  # debug mode
    cd = Line(rr[3], rr[2])  # ;cd.plot()  # debug mode
    for i in range(num + 1):
        abp = ab.line_point(i / float(num) + EPSILON)
        cdp = cd.line_point(i / float(num) + EPSILON)
        if not function:
            for hli in inter_lines(Line(abp, cdp), r):
                hli.plot()
        else:
            kwargs['function'] = function
            if base == True:
                # add back base kwarg as a line
                kwargs['base_line'] = Line(abp, cdp)
                for hli in inter_lines(Line(abp, cdp), r):
                    hli.plot(**kwargs)
            else:
                for hli in inter_lines(Line(abp, cdp), r):
                    hli.plot(**kwargs)

def rect_points(x, y, w, h, mode=CORNER):
    if mode == CENTER:
        x, y = x - w / 2.0, y - h / 2.0
    return [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]

def rotate_point(xp, yp, angle, x0=0, y0=0):
    x, y = xp - x0, yp - y0  # translate to origin
    rx = x0 + x * cos(angle) - y * sin(angle)
    ry = y0 + y * cos(angle) + x * sin(angle)
    return (rx, ry)
