from PIL import Image, ImageFilter
import os
import sys
from re import findall

arg = sys.argv[1]
print("dir: " + arg)
arg = arg.replace("\r", "")

for filename in os.listdir(arg):
    if filename.endswith(".ico"):
        removal = arg + filename
        print("Removed: " + removal)
        os.remove(removal)
    elif filename.endswith(".png"):
        size = findall(r"\d+", filename)[0]
        size = int(size)
        print(size)
        logo = Image.open(arg + filename)

        logo = logo.filter(ImageFilter.SHARPEN)

        logo.save(
            arg + filename.replace(".png", ".ico"),
            format="ICO",
            sizes=[(size, size)],
        )
