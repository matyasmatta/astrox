import PIL 
from PIL import ImageEnhance
from PIL import Image
# import the modules
import os
from os import listdir
from PIL import Image

photoID = 0
# get the path or directory
folder_dir = r"C:\Users\kiv\Documents\GitHub\astrox\elected"
for images in os.listdir(folder_dir):
    photoID += 1
    # check if the image ends with png or jpg or jpeg
    try:
        if (images.endswith(".png") or images.endswith(".jpg")\
            or images.endswith(".jpeg")):
            # display
            print(images)
            # Opens a image in RGB mode
            im = Image.open(r"C:\Users\kiv\Documents\GitHub\astrox\elected/" + images)
            left = 1515
            top = 505
            right = left+1010
            bottom = top+1515

            im1 = im.crop((left, top, right, bottom))
    except:
        pass