import msgpack


width = int(input('width: '))
height = int(input('height: '))
data = {
    'width': width,
    'height': height,
    'world1': [['.' for _ in range(width)] for _ in range(height)],
    'world2': [['.' for _ in range(width)] for _ in range(height)],
    'music': input('path to music file: '),
    'background': input('path to background: ')
}

with open("data.msgpack", "wb") as outfile:
    packed = msgpack.packb(data)
    outfile.write(packed)
