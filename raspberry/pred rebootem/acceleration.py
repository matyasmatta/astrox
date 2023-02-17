from sense_hat import SenseHat
from time import sleep


sense = SenseHat()

red = (255, 0, 0)

while True:
    acceleration = sense.get_accelerometer_raw()
    x = acceleration['x']
    y = acceleration['y']
    z = acceleration['z']

    if x<-1 or x> 1 or y<-1 or y>1 or z<0 or z>1.5:
        sense.show_letter("!", red)
    else:
        sense.clear()
    break
while True:
    compass = sense.get_compass()
    print(compass)
    sleep(0.5)