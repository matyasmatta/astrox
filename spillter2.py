import PIL 
from PIL import ImageEnhance
from PIL import Image

from PIL import Image

# Opens a image in RGB mode
im = Image.open(r"dataset\20230113df0ca6f34569672d2ec32393e9ab046c7c0afda5d4ddab8aceca8093a825150e\photo_00151_51844793137_o.jpg")
# Setting the points for cropped image
left = 1075
top = 520
right = 3015
bottom = 2460
# Cropped image of above dimension
# (It will not change original image)
im1 = im.crop((left, top, right, bottom))
# Shows the image in image viewer
im1.show()
im1.save('meta.jpg')

# Slice
infile = 'meta.jpg'
chopsize = 485

img = Image.open(infile)
width, height = img.size

# Save Chops of original image
for x0 in range(0, width, chopsize):
   for y0 in range(0, height, chopsize):
      box = (x0, y0,
             x0+chopsize if x0+chopsize <  width else  width - 1,
             y0+chopsize if y0+chopsize < height else height - 1)
      print('%s %s' % (infile, box))
      img.crop(box).save('./crop/zchop.%s.x%03d.y%03d.jpg' % (infile.replace('.jpg',''), x0, y0))