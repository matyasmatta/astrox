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
    if (images.endswith(".png") or images.endswith(".jpg")\
        or images.endswith(".jpeg")):
        # display
        print(images)
        # Opens a image in RGB mode
        im = Image.open(r"C:\Users\kiv\Documents\GitHub\astrox\elected/" + images)
        left = 16
        top = 10
        right = 4056
        bottom = 3040
        # Cropped image of above dimension
        # (It will not change original image)
        im1 = im.crop((left, top, right, bottom))
        # Shows the image in image viewer
        im1.save('meta.jpg')
        # Slice
        infile = 'meta.jpg'
        chopsize = 505

        img = Image.open(infile)
        width, height = img.size

        # Metadata
        exif = im.info['exif']
        images = images.split(sep='.jpg')

        # Save Chops of original image
        for x0 in range(0, width, chopsize):
            for y0 in range(0, height, chopsize):
                box = (x0, y0,
                        x0+chopsize if x0+chopsize <  width else  width - 1,
                        y0+chopsize if y0+chopsize < height else height - 1)
                print('%s %s' % (infile, box))

                images_path = "C:/Users/kiv/Downloads/AstroX/data_chops_elected/" + images[0] + "_x" + str(x0) + "_y" + str(y0) + ".jpg"
                if ((x0 == 2020 or x0 == 1515) and (y0 == 505 or y0 == 1010 or y0 == 1515)):
                    img.crop(box).save(images_path,exif=exif)