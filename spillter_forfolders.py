import PIL 
from PIL import ImageEnhance
from PIL import Image
# import the modules
import os
from os import listdir
from PIL import Image

photoID = 0
# get the path or directory
folder_dir = r"C:\Users\kiv\Documents\GitHub\astrox\dataset\sample_original"
for images in os.listdir(folder_dir):
    photoID += 1
    # check if the image ends with png or jpg or jpeg
    if (images.endswith(".png") or images.endswith(".jpg")\
        or images.endswith(".jpeg")):
        # display
        print(images)
        # Opens a image in RGB mode
        im = Image.open("./dataset/original/" + images)
        left = 1075
        top = 520
        right = 3015
        bottom = 2460
        # Cropped image of above dimension
        # (It will not change original image)
        im1 = im.crop((left, top, right, bottom))
        # Shows the image in image viewer
        im1.save('meta.jpg')
        # Slice
        infile = 'meta.jpg'
        chopsize = 485

        img = Image.open(infile)
        width, height = img.size

        # Metadata
        image = Image.open('./dataset/original/51844762822_3b10505c80_o.jpg')
        exif = image.info['exif']

        # Save Chops of original image
        for x0 in range(0, width, chopsize):
            for y0 in range(0, height, chopsize):
                box = (x0, y0,
                        x0+chopsize if x0+chopsize <  width else  width - 1,
                        y0+chopsize if y0+chopsize < height else height - 1)
                print('%s %s' % (infile, box))
                img.crop(box).save('./dataset/crop/zchop.%s.x%03d.y%03d.n%03d.jpg' % (infile.replace('.jpg',''), x0, y0, int(photoID)),exif=exif)