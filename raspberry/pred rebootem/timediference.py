from exif import Image
from datetime import datetime


def get_time(image):
    with open(image, 'rb') as image_file:
        img = Image(image_file)
        time_str = img.get("datetime_original")
        time = datetime.strptime(time_str, '%Y:%m:%d %H:%M:%S')
    return time
def get_time_difference(image_1, image_2):
    time_1 = get_time(image_1)
    time_2 = get_time(image_2)
    time_difference = time_2 - time_1
    print(time_1)
    print(time_2)
    print(time_difference)
    return time_difference.seconds
    
    
 

print(get_time_difference('/home/astro/Downloads/photo_00000.jpg', '/home/astro/Downloads/photo_00069.jpg'))
