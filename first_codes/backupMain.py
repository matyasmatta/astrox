#in case we don't have time to finish the complex code
#works only on Raspberry

#from Tomas


from sense_hat import SenseHat
from datetime import datetime, timedelta
from time import sleep
from csv import writer
from pathlib import Path
from picamera import PiCamera

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
    imageName = ""
    imageName = str("./img_" + str(count) + ".jpg")
    camera.capture(imageName)
    print(sense_data)
    with open("data.csv", "a", newline="") as f:
        data_writer = writer(f)
        data_writer.writerow(sense_data)
count = 0
while (datetime.now() < start_time + timedelta(minutes=5)):
    get_sense_data()
    sleep(20)
    count += 1
print("end")