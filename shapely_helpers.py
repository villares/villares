"""
From https://github.com/villares/villares/blob/main/shapely_helpers.py

Helpers to use shapely with py5

2023-07-31 Getting started with the drawing function.
2023-08-28 Testing for iterables last is less costly. Added GeoDataFrame case. Improved Point(s)
2023-10-09 Added polys_from_text() and its dependency process_glyphs
2025-05-21 clean up 
"""

from shapely import Polygon, MultiPolygon
from shapely import LineString, MultiLineString, LinearRing
from shapely import Point, MultiPoint
from shapely import GeometryCollection

try:
    from geopandas import GeoDataFrame
    geodataframe_imported = True
except ImportError:
    geodataframe_imported = False

import py5


def polys_from_text(words, font: py5.Py5Font, leading=None, alternate_spacing=False):
    """
    Produce a list of shapely Polygons (with holes!) from a string.
    New-line chars will try to move text to a new line.
    
    The alternate_spacing option will pick the glyph
    spacing from py5.text_width() for each glyph, it can be
    too spaced, but good for monospaced font alignment.
    """
    leading = leading or font.get_size()
    py5.text_font(font)
    space_width = py5.text_width(' ')
    results = []
    x_offset = y_offset = 0
    for c in words:
        if c == '\n':
            y_offset += leading
            x_offset = 0  # assuming left aligned text...
            continue
        glyph_pt_lists = [[]]
        c_shp = font.get_shape(c, 1)
        vs3 = [c_shp.get_vertex(i) for i in range(c_shp.get_vertex_count())]
        vs = set()
        for vx, vy, _ in vs3:
            x = vx + x_offset
            y = vy + y_offset
            glyph_pt_lists[-1].append((x, y))
            if (x, y) not in vs:
                vs.add((x, y))
            else:
                glyph_pt_lists.append([])  # will leave a trailling empty list
        
        if alternate_spacing:
            w = py5.text_width(c)
        else:
            w = c_shp.get_width() if vs3 else space_width
        x_offset += w
        # filter out elements with less than 3 points 
        # and stop before the trailling empty list
        glyph_polys = [Polygon(p) for p in glyph_pt_lists[:-1] if len(p) > 2]
        if glyph_polys:  # there are still empty glyphs at this point
            glyph_shapes = process_glyphs(glyph_polys)
            results.extend(glyph_shapes)
    return results


def process_glyphs(polys):
    """
    Try to subtract the shapely Polygons representing a glyph
    in order to produce appropriate looking glyphs!
    """
    polys = sorted(polys, key=lambda p: p.area, reverse=True)
    results = [polys[0]]
    for p in polys[1:]:
        # works on edge cases like â and ®
        for i, earlier in enumerate(results):
            if earlier.contains(p):
                results[i] = results[i].difference(p)
                break
        else:   # the for-loop's else only executes after unbroken loops
            results.append(p)
    return results

def draw_shapely(shps, sketch: py5.Sketch=None):
    """
    DEPRECATED!
    use py5.shape(py5.convert_cached_shape(shps)) instead.
    
    Draw most shapely objects with py5.
    This will use the "current" py5 sketch as default.
    """
    s = sketch or py5.get_current_sketch()
    if isinstance(shps, (MultiPolygon, MultiLineString, GeometryCollection)):
        for shp in shps.geoms:
            draw_shapely(shp)
    elif isinstance(shps, Polygon):
        with s.begin_closed_shape():
            s.vertices(shps.exterior.coords)
            for hole in shps.interiors:
                with s.begin_contour():
                    s.vertices(hole.coords)
    elif isinstance(shps, (LineString, LinearRing)):
        # no need to uses begin_closed_shape() because LinearRing repeats the start/end coordinates
        with s.push_style():
            s.no_fill()
            with s.begin_shape():
                s.vertices(shps.coords)
    elif isinstance(shps, Point):
        s.point(shps.x, shps.y) 
    elif isinstance(shps, MultiPoint):
        s.points((p.x, p.y) for p in shps.geoms)
    elif geodataframe_imported and isinstance(shps, GeoDataFrame):
        for shp in shps.geometry:
                draw_shapely(shp)
    else:
        try:
            for shp in shps:
                draw_shapely(shp)
        except TypeError as e:
            print(f"Unable to draw: {shps}")
            
draw_shapely_objs = draw_shapely  # para retro-compatibilidade

if __name__ == '__main__':
    def setup():
        py5.size(800, 800)
        py5.color_mode(py5.HSB)

        #py5.stroke_weight(10)
        #mp = MultiPoint([(200, 200), (100, 100), (200, 300)])
        #draw_shapely(mp)

        t = 'Oi B008!\né o gnumundo®...\n' \
            'viva a ciberlândia!\n' \
            '◍◴❂⦲జ్ఞ‌ా'
      
        d_font = py5.create_font('SansSerif', 60)
        i_font = py5.create_font('Open Sans', 60)

        shapes = polys_from_text(
            t, d_font, alternate_spacing=True)
        py5.translate(100, 100)
        for i, shp in enumerate(shapes):
            py5.fill((i * 8) % 256, 255, 255, 100)
            #draw_shapely(shp)
            py5.shape(py5.convert_shape(shp))
            
        shapes = polys_from_text(
            t, i_font, alternate_spacing=False)
        py5.translate(0, 400)
        for i, shp in enumerate(shapes):
            py5.fill((i * 8) % 256, 255, 255, 100)
            #draw_shapely(shp)
            py5.shape(py5.convert_shape(shp))



    py5.run_sketch(block=False)

