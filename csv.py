from sense_hat import SenseHat
from datetime import datetime
from csv import writer
from time import sleep

sense = SenseHat()
sense.color.gain = 60
sense.color.integration_cycles = 64


def get_sense_data():
    sense_data = []
  # Get accelerometer data
    acc = sense.get_accelerometer_raw()
    sense_data.append(round(acc["x"],4))
    sense_data.append(round(acc["y"],4))
    sense_data.append(round(acc["z"],4))
    #Get gyroscope data
    gyro = sense.get_gyroscope_raw()
    sense_data.append(round(gyro["x"],4))
    sense_data.append(round(gyro["y"],4))
    sense_data.append(round(gyro["z"],4))
    return sense_data

sense.clear((0,0
,0))

with open('nepohyb.csv', 'w', newline='') as f:
    data_writer = writer(f)
    data_writer.writerow("xyzxyz")
    for i in range (1):
        sense.clear((0,0,255))
        print(get_sense_data(), end='\n')
        data = get_sense_data()
        data_writer.writerow(data)
        sleep(0.3)
    sense.clear((255,0,0))
    sleep(0.3)
    sense.clear((255,100,100))
    sleep(0.3)
    data_writer.writerow("xyzxyz")
    for i in range (1):
        sense.clear((0,255,0))
        print(get_sense_data(), end='\n')
        data = get_sense_data()
        data_writer.writerow(data)
        sleep(0.3)
    sense.clear((255,0,0))
    sleep(0.3)
    sense.clear((255,100,100))
    sleep(0.3)
    for i in range (1):
        sense.clear((255,0,0))
        print(get_sense_data(), end='\n')
        data = get_sense_data()
        data_writer.writerow(data)
        sleep(0.3)
    sense.clear((0,
    0,0))
