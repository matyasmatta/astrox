from sense_hat import SenseHat
from datetime import datetime
from csv import writer
from time import sleep

sense = SenseHat()
sense.color.gain = 60
sense.color.integration_cycles = 64


def get_sense_data():
    sense_data = []
    #moje
    d = sense.get_orientation_degrees()
    sense_data.append(round(d["yaw"],4))
    r = sense.get_orientation_radians()
    sense_data.append(round(r["yaw"],4))
    return sense_data

sense.clear((0,0,0))
c=255
with open('noninternet.csv', 'w', newline='') as f:
    data_writer = writer(f)
    data_writer.writerow("dr")
    for i in range (64):
        data = get_sense_data()
        data_writer.writerow(data)
        print("idk")
        c=c-4
        sense.clear(c,0,0) 
          
            


    
    