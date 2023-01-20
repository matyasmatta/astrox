from sense_hat import SenseHat
import time
 
sense = SenseHat()
 
while True:
    orientation = sense.get_orientation()
    p=round(orientation["pitch"], 0)
    r=round(orientation["roll"], 0)
    y=round(orientation["yaw"], 0)
    print("p: %s, r: %s, y: %s" % (p,r,y))
    time.sleep(1)
