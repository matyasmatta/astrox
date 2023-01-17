from split_image import split_image
import PIL 
from PIL import ImageEnhance

img = PIL.Image.open('photo.jpg')
#converter = PIL.ImageEnhance.Color(img)
#img2 = converter.enhance(10)
#img2.show()
converter2 = PIL.ImageEnhance.Sharpness(img)
img3 = converter2.enhance(10)
img3.show()
img.save("photo3.jpg")


split_image("photo3.jpg", 15, 15, True, False, "./data_legacy/")