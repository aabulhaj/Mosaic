import os

from PIL import Image


def _pil_image_from_lists(image_as_lists):
    height = len(image_as_lists)
    width = min([len(image_as_lists[i]) for i in range(height)])

    image = Image.new("RGB", (width, height))
    for i in range(width):
        for j in range(height):
            image.putpixel((i, j), image_as_lists[j][i])
    return image


def _lists_from_pil_image(image):
    width, height = image.size
    pixels = list(image.getdata())
    return [pixels[i * width:(i + 1) * width] for i in range(height)]


def build_tile_base(tiles_dir, tile_height):
    tiles = []
    widths = []
    for file in os.listdir(tiles_dir):
        try:
            image = Image.open(os.path.join(tiles_dir, file))
            if image.mode != 'RGB':
                image = image.convert(mode='RGB')
            img_ratio = image.size[0] / image.size[1]
            image = image.resize((int(img_ratio * tile_height), tile_height), Image.ANTIALIAS)
            tiles.append(_lists_from_pil_image(image))
            widths.append(image.size[0])
        except IOError:
            pass

    min_width = min(widths)
    cropped_tiles = []

    for tile in tiles:
        cropped = []
        for row in range(tile_height):
            new_row = tile[row][: min_width]
            cropped += [new_row]
        cropped_tiles += [cropped]

    return cropped_tiles


def load_image(image_filename):
    pil_image = Image.open(image_filename)
    return _lists_from_pil_image(pil_image)


def save(image, filename):
    mosaic = _pil_image_from_lists(image)
    output_dir = os.path.dirname(filename)

    if os.path.exists(filename):
        print("Error: can not save to file: ", filename, ". File already exists.")
        return

    if output_dir != "" and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    mosaic.save(filename)


def show(image):
    mosaic = _pil_image_from_lists(image)
    mosaic.show()
