from PIL import Image
import math

def color_distance(c1: tuple[int, int, int], c2: tuple[int, int, int]) -> float:
    return math.sqrt(
        (c1[0] - c2[0]) ** 2 +
        (c1[1] - c2[1]) ** 2 +
        (c1[2] - c2[2]) ** 2
    )

def remove_solid_background(
    image: Image.Image,
    tolerance: int = 35,
    edge_softness: int = 10
) -> Image.Image:
    img = image.copy().convert("RGBA")
    pixels = img.load()

    width, height = img.size

    # 默认取左上角像素作为背景色
    bg_color = pixels[0, 0][:3]

    for y in range(height):
        for x in range(width):
            r, g, b, a = pixels[x, y]
            dist = color_distance((r, g, b), bg_color)

            if dist <= tolerance:
                pixels[x, y] = (r, g, b, 0)

            elif edge_softness > 0 and dist <= tolerance + edge_softness:
                alpha_ratio = (dist - tolerance) / edge_softness
                new_alpha = int(a * alpha_ratio)
                pixels[x, y] = (r, g, b, new_alpha)

    return img