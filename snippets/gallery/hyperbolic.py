import math

from drawsvg import Drawing
from hyperbolic.poincare import *
from hyperbolic.poincare.util import triangle_side_for_angles
import hyperbolic.tiles as htiles


p1 = 4
p2 = 3
q = 3
rotate = 0

theta1, theta2 = math.pi*2/p1, math.pi*2/p2
phi_sum = math.pi*2/q
r1 = triangle_side_for_angles(theta1/2, phi_sum/2, theta2/2)
r2 = triangle_side_for_angles(theta2/2, phi_sum/2, theta1/2)

t_gen1 = htiles.TileGen.make_regular(p1, hr=r1, skip=1)
t_gen2 = htiles.TileGen.make_regular(p2, hr=r2, skip=1)

t_layout = htiles.TileLayout()
t_layout.add_generator(t_gen1, (1,)*p1)
t_layout.add_generator(t_gen2, (0,)*p2, htiles.TileDecoratorNull())
start_tile = t_layout.default_start_tile(rotate_deg=rotate)

t1 = start_tile
t2 = t_layout.place_tile(t1.sides[-1])
t3 = t_layout.place_tile(t2.sides[-1])
point_base = t3.vertices[-1]
points = [Transform.rotation(deg=-i*360/p1).apply_to_point(point_base)
          for i in range(p1)]
vertices = start_tile.vertices
edges = []
for i, point in enumerate(points):
    v1 = vertices[i]
    v2 = vertices[(i+1)%p1]
    edge = Hypercycle.from_points(*v1, *v2, *point, segment=True, exclude_mid=True)
    edges.append(edge)
decorate_poly = Polygon(edges=edges, vertices=vertices)
decorator1 = htiles.TileDecoratorPolygons(decorate_poly)
t_layout.set_decorator(decorator1, 0)

start_tile = t_layout.default_start_tile(rotate_deg=rotate)
tiles = t_layout.tile_plane(start_tile, depth=6)

d = Drawing(2, 2, origin='center')
#d.draw(euclid.Circle(0, 0, 1), fill='silver')
for tile in tiles:
    d.draw(tile, hwidth=0.02, fill='red')
tiles[0].decorator = None
d.draw(
    Hypercycle.from_points(
        *tiles[0].vertices[0], *tiles[0].vertices[1], *point_base
    ),
    hwidth=0.02,
    fill='black',
)

d.set_render_size(w=400)
print(d.as_svg())
