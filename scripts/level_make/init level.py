import msgpack
import os

level_name = input("Level name: ")
os.mkdir(f'../../games/S2W Adventure/levels/{level_name}')
os.chdir(f'../../games/S2W Adventure/levels/{level_name}')
width = int(input('width: '))
height = int(input('height: '))
data = {
    'width': width,
    'height': height,
    'world1': [['.' for _ in range(width)] for _ in range(height)],
    'world2': [['.' for _ in range(width)] for _ in range(height)],
    'music': f'music/{level_name}-level_sound',
    'background': f'images/{level_name}-level_background'
}

with open("level.msgpack", "wb") as outfile:
    packed = msgpack.packb(data)
    outfile.write(packed)
