import math
import sys

import utils


def compare_pixels(pixel1, pixel2):
    return abs(pixel1[0] - pixel2[0]) + abs(pixel1[1] - pixel2[1]) + abs(pixel1[2] - pixel2[2])


def compare_images(image1, image2):
    pixels_diff = 0
    for row in range(min(len(image1), len(image2))):
        for col in range(min(len(image1[0]), len(image2[0]))):
            pixels_diff += compare_pixels(image1[row][col], image2[row][col])
    return pixels_diff


def get_piece(image, upper_left, size):
    piece = []
    for row in range(upper_left[0], min(upper_left[0] + size[0], len(image))):
        piece_row = []
        for col in range(upper_left[1], min(upper_left[1] + size[1], len(image[0]))):
            piece_row += [image[row][col]]
        piece += [piece_row]
    return piece


def set_piece(image, upper_left, piece):
    for row in range(upper_left[0], min(upper_left[0] + len(piece), len(image))):
        for col in range(upper_left[1], min(upper_left[1] + len(piece[0]), len(image[0]))):
            image[row][col] = piece[row - upper_left[0]][col - upper_left[1]]


def pixels_average(image):
    pixels = 0
    red = 0
    green = 0
    blue = 0

    for row in range(len(image)):
        for col in range(len(image[0])):
            pixels += 1
            red += image[row][col][0]
            green += image[row][col][1]
            blue += image[row][col][2]

    return red / pixels, green / pixels, blue / pixels


def preprocess_tiles(tiles):
    return [pixels_average(tile) for tile in tiles]


def get_best_tiles(objective, tiles, averages, num_candidates):
    candidate_tiles = []

    avg_obj = pixels_average(objective)

    for dif in range(255):
        for i in range(len(tiles)):
            if len(candidate_tiles) == num_candidates:
                break

            if avg_obj[0] - dif <= averages[i][0] <= avg_obj[0] + dif \
                    and avg_obj[1] - dif <= averages[i][1] <= avg_obj[1] + dif \
                    and avg_obj[2] - dif <= averages[i][2] <= avg_obj[2] + dif \
                    and tiles[i] not in candidate_tiles:
                candidate_tiles.append(tiles[i])
    return candidate_tiles


def choose_tile(piece, tiles):
    best_tile = None
    best_tile_pixels_sum = 0
    for tile in tiles:
        tile_pixels_sum = compare_images(piece, tile)
        if tile_pixels_sum < best_tile_pixels_sum or not best_tile:
            best_tile = tile
            best_tile_pixels_sum = tile_pixels_sum
    return best_tile


def make_mosaic(image, tiles, num_candidates):
    tiles_averages = preprocess_tiles(tiles)
    size = (len(tiles[0]), len(tiles[0][0]))

    for row in range(int(math.ceil(len(image) / size[0]))):
        for col in range(int(math.ceil(len(image[0]) / size[1]))):
            upper_left = (row * size[0], col * size[1])
            piece = get_piece(image, upper_left, size)
            best_tiles = get_best_tiles(piece, tiles, tiles_averages, num_candidates)
            best_tile = choose_tile(piece, best_tiles)
            set_piece(image, upper_left, best_tile)
    return image


if __name__ == '__main__':
    if len(sys.argv) != 6:
        print('Usage: python3 mosaic.py <image_source> <images_dir> <output_name> <tile_height> <num_candidates>')
        exit()

    image_source = sys.argv[1]
    images_dir = sys.argv[2]
    output_name = sys.argv[3]
    tile_height = int(sys.argv[4])
    num_candidate = int(sys.argv[5])

    image = utils.load_image(image_source)
    tiles = utils.build_tile_base(images_dir, tile_height)

    mosaic_image = make_mosaic(image, tiles, num_candidate)
    utils.save(mosaic_image, output_name)
