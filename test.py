import os
from os import listdir
import PIL 
from PIL import ImageEnhance
from PIL import Image
# import the modules
import os
from os import listdir
from PIL import Image 

# get the path or directory
folder_dir = r"C:\Users\kiv\Documents\GitHub\astrox\dataset\sample_original"
for images in os.listdir(folder_dir):
 
    # check if the image ends with png or jpg or jpeg
    if (images.endswith(".png") or images.endswith(".jpg")\
        or images.endswith(".jpeg")):
        # display
        print(images)
        im = Image.open(r"./dataset/original/51844762822_3b10505c80_o.jpg")
        im.show()
        