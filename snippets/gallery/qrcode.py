import qrcode
from qrcode.image.svg import SvgPathImage

img = qrcode.make("https://github.com/sponsors/lincolnloop", box_size=20, border=2, image_factory=SvgPathImage)
print(f'<div>{img.to_string().decode("utf8")}</div>')
