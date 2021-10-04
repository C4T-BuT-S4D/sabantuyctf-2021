#!/usr/bin/env python3

from io import BytesIO
from PIL import Image, ImageDraw, ImageFont


def make_flag_image(flag: str) -> Image:
    path = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf'
    size = 20

    font = ImageFont.truetype(path, size)
    width, height = font.getsize(flag)

    padding = 5
    box = (width + padding * 2, height + padding * 2)

    background = (0, 0, 0)
    foreground = (255, 255, 255)

    img = Image.new('RGB', box, background)

    draw = ImageDraw.Draw(img)
    draw.text((padding, padding), flag, foreground, font)

    return img


def main():
    with open('flag.txt', 'r') as file:
        flag = file.read().strip()

    with BytesIO() as buffer:
        with make_flag_image(flag) as img:
            # img.show()
            img.save(buffer, 'PNG')

        data = buffer.getvalue()

    data += b'\x00' * (3 - len(data) % 3)

    with Image.open('container.png') as container:
        width, height = container.size

        for i in range(len(data) // 3):
            xy = (i % width, i // width)
            pixel = tuple(data[3*i:3*i+3])
            container.putpixel(xy, pixel)

        container.save('bliss.png', 'PNG')

    return


if __name__ == '__main__':
    main()
