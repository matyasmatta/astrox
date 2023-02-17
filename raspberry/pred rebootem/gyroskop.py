from sense_hat import SenseHat
from time import sleep

sense = SenseHat()

red = (255, 0, 0)

while True:
    gyro = sense.get_gyroscope_raw()
    x = gyro['x']
    y = gyro['y']
    z = gyro['z']

    print(round(x,3), round(y,3), round(z,3))
    for event in sense.stick.get_events():
        if  event.action == "pressed":
            print("necolasfjksdklůfjlsdfjlkasdjfl")
    
    

