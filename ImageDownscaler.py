from PIL import Image, ImageFilter
import os
import sys

srcPath = sys.argv[1]
expPath = sys.argv[2]
ScaleX = int(sys.argv[3])
ScaleY = int(sys.argv[4])

for filename in os.listdir(expPath):
    if not filename.endswith(".png"):
        continue
    else:
        os.remove(expPath + filename)

for filename in os.listdir(srcPath):
    if filename.endswith(".png"):
        img = Image.open(srcPath + filename)
        print(img)

        newsize = (ScaleX, ScaleY)
        img.thumbnail(newsize)

        img.save(
            expPath + filename,
            format="PNG",
            sizes=[(ScaleX, ScaleY)],
        )
