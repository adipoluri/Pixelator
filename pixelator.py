import math
import requests
import json
from PIL import Image
from progress.bar import Bar


############################################################
# Pixelate function from https://github.com/RPOD/Pixelator #
############################################################
def meanPixel(tile):
    rt = 0
    gt = 0
    bt = 0
    for pixel in tile:
        r, g, b = pixel
        rt = rt + r
        gt = gt + g
        bt = bt + b
    mean = [math.floor(rt / len(tile)), math.floor(gt / len(tile)), math.floor(bt / len(tile))]
    return mean


def pixelate(image, pixelSize, scale, outputName):
    width, height = image.size
    image = image.convert('RGB')
    hr = math.ceil(height / int(pixelSize))
    wr = math.ceil(width / int(pixelSize))
    tiles = [[[] for i in range(hr)] for j in range(wr)]
    for x in range(width):
        for y in range(height):
            tiles[math.floor(x / pixelSize)][math.floor(y / pixelSize)].append(image.getpixel((x, y)))
    meanArray = [([0] * hr) for k in range(wr)]
    for metaX in range(wr):
        for metaY in range(hr):
            meanArray[metaX][metaY] = meanPixel(tiles[metaX][metaY])
    pixelData = image.load()
    for x in range(width):
        for y in range(height):
            r = meanArray[math.floor(x / pixelSize)][math.floor(y / pixelSize)][0]
            g = meanArray[math.floor(x / pixelSize)][math.floor(y / pixelSize)][1]
            b = meanArray[math.floor(x / pixelSize)][math.floor(y / pixelSize)][2]
            pixelData[x, y] = (r, g, b)
    if not scale == 100:
        image = image.resize((int(width * scale / 100), int(height * scale / 100)), Image.ANTIALIAS)
    image.save(outputName, 'PNG')


def getImage(index, name):
    url = index
    filename = name + ".png"
    r = requests.get(url, allow_redirects=True)
    open("out/" + filename, 'wb').write(r.content)
    pixelate(Image.open("out/" + filename), 3, 100, "out/" + filename)


def main():
    exists = False
    while not exists:
        file = input('What Json File would you like to Pixelate? ')
        try:
            with open("in/" + file) as f:
                data = json.load(f)
                exists = True
        except FileNotFoundError as e:
            exists = False

    bar = Bar("Converting Images", max=len(data))
    for ind in data:
        getImage(ind["icon"], ind["uid"])
        bar.next()
    bar.finish()


main()
