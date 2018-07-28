import os
import sys

from PIL import Image

def extract_edof(fname):
    file = open(fname, 'rb')
    data = file.read()
    file.close()

    data = data.split(b'edof')[-1]
    data = data.split(b'DepthEn')[0]

    c = int.from_bytes(data[16:18], 'little')
    r = int.from_bytes(data[18:20], 'little')

    img = Image.frombuffer('L', (c, r), data[68:], 'raw', 'L', 0, 0)

    o = data[7]
    if o == 0x10:
        img = img.transpose(Image.FLIP_TOP_BOTTOM)
    elif o == 0x12:
        img = img.transpose(Image.FLIP_LEFT_RIGHT)
    elif o == 0x13:
        img = img.transpose(Image.TRANSPOSE)

    new_fname = fname.split('.')[0] + '_edof.jpg'
    print(new_fname)
    img.save(new_fname)

if __name__ == '__main__':
    # no argument
    if len(sys.argv) < 2:
        print('No file specified')
    elif len(sys.argv) == 2:
        # file
        if os.path.isfile(sys.argv[1]):
            print('file')
            files = [sys.argv[1]]
        # folder
        else:
            print('folder')
            files = os.listdir(sys.argv[1])
            files = [sys.argv[1] + '/' + i for i in files]
    # multiple files
    else:
        print('multiple files')
        files = sys.argv[1:]

    for f in files:
        extract_edof(f)
