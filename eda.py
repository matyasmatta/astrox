from sense_hat import SenseHat
from time import sleep

sense = SenseHat()
#north = sense.get_compass()
#print("North: %s" % north)

# alternatives
#print(sense.compass)

#AstroX20220113

while True:
    acceleration = sense.get_accelerometer_raw()
    x = acceleration["x"]
    y = acceleration["y"]
    z = acceleration["z"]

    x=round(x, 5)
    y=round(y, 5)
    z=round(z, 5)
    print(x, y, z)
    sleep(0.5)
