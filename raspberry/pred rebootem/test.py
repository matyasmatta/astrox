from sense_hat import SenseHat
import time

while True:
    sense = SenseHat()
    north = sense.get_compass()
    # alternatives
    print(sense.compass)
    time.sleep(0.1)
    heading = sense.get_compass()
    if heading < 45 or heading > 315:
        sense.show_letter('N') 
    elif heading < 135:
        sense.show_letter('E') 
    elif heading < 225:
        sense.show_letter('S') 
    else:
        sense.show_letter("W")

