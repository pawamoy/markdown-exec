import math
import numpy as np

import drawsvg as draw
from drawsvg import Drawing
from hyperbolic import euclid
from hyperbolic.poincare import *
from hyperbolic.poincare.util import (
    radial_euclid_to_poincare, triangle_side_for_angles,
)
import hyperbolic.tiles as htiles
 

# Control the orientation that tiles are placed together
class TileLayoutIsosceles(htiles.TileLayout):
    def calc_gen_index(self, code):
        ''' Controls which type of tile to place '''
        return 0
    def calc_tile_touch_side(self, code, gen_index):
        ''' Controls tile orientation '''
        try:
            side, colors = code
            return 2 - side
        except TypeError:
            return 0
    def calc_side_codes(self, code, gen_index, touch_side, default_codes):
        ''' Controls tile side codes '''
        try:
            side, colors = code
            # 0=red, 1=orange, 2=yellow, 3=lime, 4=green, 5=blue, 6=pink
            if side != 1:
                if side == 0: shift = -1
                elif side == 2: shift = 1
                else: shift = 0
                nc = len(colors)
                new_colors = [colors[(i+shift)%nc] for i in range(nc)]
            else:
                new_colors = [colors[0], colors[1], colors[6], colors[4],
                    colors[3], colors[5], colors[2]]
        except TypeError:
            nc = q1
            new_colors = [(i+code)%nc for i in range(nc)]
        return [(side, new_colors) for side in range(3)]

q1 = 7  # Number of polygons around some points
q2 = 6  # Number of polygons around other points
depth = 10  # How far from the center to draw tiles

# Calculate isosceles triangle
assert q2 > 4 and q2 % 2 == 0, 'q2 must be even and at least 6'
phi1, phi2 = math.pi*2/q1, math.pi*2/q2
# Side lengths
s0 = triangle_side_for_angles(phi1, phi2, phi2)
s1 = triangle_side_for_angles(phi2, phi2, phi1)
s2 = s0
pt0 = Point.from_h_polar(0,0)
pt1 = Point.from_h_polar(s0,0)
pt2 = Point.from_h_polar(s2,-phi1)
# Circumcircle
circumcirc = euclid.Circle.from_points(*pt0, *pt1, *pt2)
r = radial_euclid_to_poincare(circumcirc.r)
pt_center = Point.from_euclid(circumcirc.cx, circumcirc.cy)
# Translate triangle to center
trans_center = Transform.shift_origin(pt_center, pt0)
ptc0, ptc1, ptc2 = trans_center(pt0, pt1, pt2)
center_points = (ptc0, ptc1, ptc2)
tile = htiles.Tile(center_points)

# Calculate weave width
# For right triangle: tan(A) = tanh(opp) / sinh(adj)
# => opp = atanh(tan(A) * sinh(adj))
r_insc = math.atanh(math.tan(phi2/2) * math.sinh(s1/2))  # Inscribed circle radius
h = math.atanh(math.tan(phi2) * math.sinh(s1/2))  # Triangle height
center_diff = r - (h - r_insc)

t_gen = htiles.TileGen.from_center_tile(tile)

decorator_late = htiles.TileDecoratorLateInit()

t_layout = TileLayoutIsosceles()
t_layout.add_generator(t_gen, (0,)*4, decorator_late)
start_tile = t_layout.start_tile(code=2,rotate_deg=0,center_corner=False)

tiles = t_layout.tile_plane(start_tile, depth=depth)

def draw_tiles(drawing, tiles):
    for tile in tiles:
        tile.decorator = None
        d.draw(tile, hwidth=0.02, fill='white')
    for tile in tiles:
        d.draw(tile, draw_verts=True, hradius=0.05, hwidth=0.02,
                     fill='black', opacity=0.6)
        
d = draw.Drawing(2, 2, origin='center')
d.draw(euclid.Circle(0, 0, 1), fill='#ddd')
draw_tiles(d, tiles)

d.set_render_size(w=400)
print(d.as_svg())
