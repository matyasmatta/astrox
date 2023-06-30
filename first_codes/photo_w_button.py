#this should make photo when you press joystick
#works on Raspberry

#by Eda

from datetime import datetime, timedelta
from time import sleep
from csv import writer
from pathlib import Path
from picamera import PiCamera

from sense_hat import SenseHat
from time import sleep
sense = SenseHat()

e = (0, 0, 0)
w = (255, 255, 255)

sense.clear()

       
base_folder = Path(__file__).parent.resolve()
camera = PiCamera()
camera.resolution = (4056, 3040)
sleep(2)
x=100

while x < 999:
    imageName = ""
    imageName = str("./img_" + str(x) + ".jpg")
    while True:
        for event in sense.stick.get_events():
        # Check if the joystick was pressed
            if event.action == "pressed":
                    camera.capture(imageName)
                    x=x+1
