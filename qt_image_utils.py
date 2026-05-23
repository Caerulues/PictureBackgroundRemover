from PIL import Image
from PySide6.QtGui import QImage, QPixmap


def pil_to_qpixmap(image: Image.Image) -> QPixmap:
    image = image.convert("RGBA")
    data = image.tobytes("raw", "RGBA")

    qimage = QImage(
        data,
        image.width,
        image.height,
        image.width * 4,
        QImage.Format.Format_RGBA8888
    )

    return QPixmap.fromImage(qimage)


def make_checkerboard(
    size: tuple[int, int],
    block_size: int = 20
) -> Image.Image:
    width, height = size
    img = Image.new("RGBA", size, (255, 255, 255, 255))
    pixels = img.load()

    for y in range(height):
        for x in range(width):
            if (x // block_size + y // block_size) % 2 == 0:
                pixels[x, y] = (210, 210, 210, 255)
            else:
                pixels[x, y] = (245, 245, 245, 255)

    return img


def make_preview(
    image: Image.Image,
    max_size: tuple[int, int] = (650, 520)
) -> QPixmap:
    preview = image.copy().convert("RGBA")
    preview.thumbnail(max_size, Image.LANCZOS)

    checker = make_checkerboard(preview.size)
    checker.alpha_composite(preview)

    return pil_to_qpixmap(checker)