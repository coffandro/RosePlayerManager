from PIL import Image, ImageFilter
import os
from re import findall

for filename in os.listdir("Icons"):
    if filename.endswith(".ico"):
        removal = "Icons/" + filename
        print("Removed: " + removal)
        os.remove(removal)
    elif filename.endswith(".png"):
        size = findall(r'\d+',filename)[0]
        size = int(size)
        print(size)
        logo = Image.open("Icons/" + filename)
        
        logo = logo.filter(ImageFilter.SHARPEN)
 
        logo.save("Icons/" + filename.replace(".png",".ico"), format='ICO', sizes=[(size, size)])
