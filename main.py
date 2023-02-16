import os
import pathlib
from pycoral.utils import edgetpu
from pycoral.utils import dataset
from pycoral.adapters import common
from pycoral.adapters import classify
from PIL import Image
import ai
import stiny_maty

try:
    image = 'zchop.meta.x000.y000.n004.jpg'
    data = ai.ai_model(image)
    print(data)
    counter_for_shadows = 0
    angle = 317
    while True:
        try:
            x_max = data[counter_for_shadows]['xmax']
            y_max = data[counter_for_shadows]['ymax']
            x_min = data[counter_for_shadows]['xmin']
            y_min = data[counter_for_shadows]['ymin']
            print(x_min, y_min, x_max, y_max)

            x_centre_of_cloud = (x_min+x_max)/2
            y_centre_of_cloud = (y_min+y_max)/2
            x_centre_of_cloud = round(x_centre_of_cloud, 0)
            y_centre_of_cloud = round(y_centre_of_cloud, 0)
            x_centre_of_cloud = int(x_centre_of_cloud)
            y_centre_of_cloud = int(y_centre_of_cloud)

            print(x_centre_of_cloud, y_centre_of_cloud)
            data[counter_for_shadows]['shadow'] = stiny_maty.calculate_shadow(image, x_centre_of_cloud, y_centre_of_cloud, angle)
            print("Cloud number", counter_for_shadows, "has a lenght of", data[counter_for_shadows]['shadow'])
            counter_for_shadows += 1
        except:
            break
except:
    print("code failed")