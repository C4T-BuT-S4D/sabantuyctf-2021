#!/usr/bin/env python3

from PIL import Image


def main():
    img = []

    with Image.open('bliss.png') as bliss:
        width, height = bliss.size

        for i in range(width * height):
            r, g, b = bliss.getpixel((i % width, i // width))
            img.extend([r, g, b])

    with open('flag.png', 'wb') as file:
        file.write(bytes(img))

    return


if __name__ == '__main__':
    main()
