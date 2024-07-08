from tempfile import NamedTemporaryFile
from chalk import Diagram, triangle, unit_x
from colour import Color

papaya = Color("#ff9700")

def sierpinski(n: int, size: int) -> Diagram:
    if n <= 1:
        return triangle(size)
    else:
        smaller = sierpinski(n - 1, size / 2)
        return smaller.above(smaller.beside(smaller, unit_x).center_xy())

d = sierpinski(5, 4).fill_color(papaya)

# Chalk doesn't provide an easy method to get a string directly,
# so we use a temporary file.
with NamedTemporaryFile("w+") as tmpfile:
    d.render_svg(tmpfile.name, height=256)
    tmpfile.seek(0)
    svg = tmpfile.read()

print(svg)
