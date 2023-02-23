from sense_hat import SenseHat
from datetime import datetime, timedelta
from time import sleep
from csv import writer
from pathlib import Path
from picamera import PiCamera
from orbit import ISS
import sever_eda

base_folder = Path(__file__).parent.resolve()
data_file = base_folder / "data.csv"
sense = SenseHat()
sense.color.gain = 60
sense.color.integration_cycles = 64
start_time = datetime.now()
now_time = datetime.now()
camera = PiCamera()
camera.resolution = (4056, 3040)
sleep(2)

with open('data.csv', 'w', buffering=1, newline='') as f:
    data_writer = writer(f)
    data_writer.writerow(['temp', 'pres', 'hum',
                          'red', 'green', 'blue', 'clear', #only for Sense HAT version 2
                          'yaw', 'pitch', 'roll',
                          'mag_x', 'mag_y', 'mag_z',
                          'acc_x', 'acc_y', 'acc_z',
                          'gyro_x', 'gyro_y', 'gyro_z',
                          'datetime'])
def convert(angle):
    sign, degrees, minutes, seconds = angle.signed_dms()
    exif_angle = f'{degrees:.0f}/1,{minutes:.0f}/1,{seconds*10:.0f}/10'
    return sign < 0, exif_angle

def get_photo(camera):
    location = ISS.coordinates()

    # Convert the latitude and longitude to EXIF-appropriate representations
    south, exif_latitude = convert(location.latitude)
    west, exif_longitude = convert(location.longitude)

    # Set the EXIF tags specifying the current location
    camera.exif_tags['GPS.GPSLatitude'] = exif_latitude
    camera.exif_tags['GPS.GPSLatitudeRef'] = "S" if south else "N"
    camera.exif_tags['GPS.GPSLongitude'] = exif_longitude
    camera.exif_tags['GPS.GPSLongitudeRef'] = "W" if west else "E"

    # Capture the image
    imageName = ""
    imageName = str("./img_" + str(count) + ".jpg")
    camera.capture(imageName)


def get_sense_data():
    sense_data = []

    # Get environmental data
    sense_data.append(sense.get_temperature())
    sense_data.append(sense.get_pressure())
    sense_data.append(sense.get_humidity())
    # Get colour sensor data (version 2 Sense HAT only)
    red, green, blue, clear = sense.colour.colour
    sense_data.append(red)
    sense_data.append(green)
    sense_data.append(blue)
    sense_data.append(clear)
    # Get orientation data
    orientation = sense.get_orientation()
    sense_data.append(orientation["yaw"])
    sense_data.append(orientation["pitch"])
    sense_data.append(orientation["roll"])
    # Get compass data
    mag = sense.get_compass_raw()
    sense_data.append(mag["x"])
    sense_data.append(mag["y"])
    sense_data.append(mag["z"])
    # Get accelerometer data
    acc = sense.get_accelerometer_raw()
    sense_data.append(acc["x"])
    sense_data.append(acc["y"])
    sense_data.append(acc["z"])
    #Get gyroscope data
    gyro = sense.get_gyroscope_raw()
    sense_data.append(gyro["x"])
    sense_data.append(gyro["y"])
    sense_data.append(gyro["z"])
    sense_data.append(datetime.now())
    get_photo(camera)
    #print(sense_data)
    with open("data.csv", "a", newline="") as f:
        data_writer = writer(f)
        data_writer.writerow(sense_data)
count = 0
while (datetime.now() < start_time + timedelta(minutes=4.3)):
    get_sense_data()
    print(datetime.now())
    i_1=str(count)
    before = "eda\direction12\photo_18"
    image_1=str(before + i_1 +".jpg")
    i_2=str(count+1)
    #print(image_1)
    image_2=str(before + i_2 +".jpg")
    #print(image_2)

    data = sever_eda.find_north(image_1, image_2)
    #print(data)
    count+=1
    sleep(3)
    count += 1
    
print("konec")