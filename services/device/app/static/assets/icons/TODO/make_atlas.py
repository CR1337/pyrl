import json
from math import ceil, sqrt
from os import listdir
from os.path import isfile

from PIL import Image

ICON_WIDTH = 100
ICON_HEIGHT = 100

icon_filenames = [
    filename
    for filename in listdir()
    if isfile(filename) and filename.endswith(".png")
]
icon_count = len(icon_filenames)
atlas_width = ceil(sqrt(icon_count))
atlas_height = ceil(icon_count / atlas_width)

atlas = Image.new(
    'RGB', (atlas_width * ICON_WIDTH, atlas_height * ICON_HEIGHT)
)
atlas_dict = {}

done = False
for y in range(atlas_height):
    for x in range(atlas_width):
        index = y * atlas_width + x
        if index > icon_count - 1:
            done = True
            break
        icon_filename = icon_filenames[index]
        with open(icon_filename, 'rb') as file:
            icon = Image.open(file, 'r', formats=['png'])
            offset = (x * ICON_WIDTH, y * ICON_HEIGHT)
            atlas.paste(icon, offset)
        atlas_dict[icon_filename.split(".")[0]] = list(offset)
    if done:
        break

with open("atlas.png", 'wb') as file:
    atlas.save(file, bitmap_format='png')

with open("atlas_offsets.json", 'w') as file:
    json.dump(atlas_dict, file)
