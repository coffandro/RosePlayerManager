from PIL import Image, ImageFilter
import os
import sys
from re import findall

arg = sys.argv[1]
ScaleX = sys.argv[2]
ScaleY = sys.argv[3]

for filename in os.listdir(arg):
    if filename.endswith(".png"):
        logo = Image.open(arg + filename)

        logo = logo.thumbnail((ScaleX, ScaleY))

        logo.save(
            arg + filename,
            format="PNG",
            sizes=[(sizeX, sizeY)],
        )
