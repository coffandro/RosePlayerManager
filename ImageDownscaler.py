from PIL import Image, ImageFilter
import os
import sys

arg = sys.argv[1]
ScaleX = int(sys.argv[2])
ScaleY = int(sys.argv[3])

for filename in os.listdir(arg):
    if filename.endswith("FR.png"):
        os.remove(arg + filename.replace("FR.png", ".png"))
        print(filename)
        img = Image.open(arg + filename)
        print(img)

        newsize = (ScaleX, ScaleY)
        img.thumbnail(newsize)

        img.save(
            arg + filename.replace("FR.png", ".png"),
            format="PNG",
            sizes=[(ScaleX, ScaleY)],
        )
