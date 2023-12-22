from PIL import Image, ImageFilter
from os import listdir
from re import findall

for filename in listdir("Icons"):
    if filename.endswith(".png"):
        size = findall(r'\d+',filename)[0]
        size = int(size)
        print(size)
        logo = Image.open("Icons/" + filename)
        
        logo = logo.filter(ImageFilter.SHARPEN)
 
        logo.save("Icons/" + filename.replace(".png",".ico"), format='ICO', sizes=[(size, size)])
