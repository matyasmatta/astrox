from PIL import Image
image = Image.open("52652396850_976568dfb4_o.jpg")
rotated_image = image.rotate(160)
rotated_image.show()