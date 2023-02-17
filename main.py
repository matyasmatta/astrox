import os
import pathlib
from pycoral.utils import edgetpu
from pycoral.utils import dataset
from pycoral.adapters import common
from pycoral.adapters import classify
from PIL import Image
import ai
import stiny_maty3

try:
    try:
        image = 'zchop.meta.x000.y000.n011.jpg'
        image_id = 2
    except:
        print("There was an error loading image, make sure that path is set up correctly and do not forget to specify the filetype suffix.")
    try:
        data = ai.ai_model(image)
    except:
        print("Module AI failed, make sure that Coral TPU is connected to computer properly, else contect developer.")
    print(data)
    counter_for_shadows = 0
    angle = 320
    os.remove('pixels.csv')
    create_new_pixels_csv = open("pixels.csv", "x")
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

            x_cloud_lenght = abs(x_max - x_min)
            y_cloud_lenght = abs(y_max - y_min)

            if x_cloud_lenght < 69 and y_cloud_lenght < 69:
                try:
                    data[counter_for_shadows]['shadow'] = stiny_maty3.calculate_shadow(image, x_centre_of_cloud, y_centre_of_cloud, angle, cloud_id=counter_for_shadows, image_id=image_id)
                except:
                    print("There was an error running the stiny module.")
                print("Cloud number", counter_for_shadows, "has a lenght of", data[counter_for_shadows]['shadow'])
            else:
                print("Cloud number", counter_for_shadows, "did not meet maximal lenght criteria")
            counter_for_shadows += 1
        except:
            meta = Image.open('meta.jpg')
            meta.show()
            break
except:
    print("Code failed")