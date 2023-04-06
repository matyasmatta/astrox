from datetime import datetime, timedelta
from time import sleep
from csv import writer
from pathlib import Path
from picamera import PiCamera
import pygame

pygame.init()

# to spam the pygame.KEYDOWN event every 100ms while key being pressed
pygame.key.set_repeat(100, 100)

base_folder = Path(__file__).parent.resolve()
camera = PiCamera()
camera.resolution = (4056, 3040)
sleep(2)
x=100

while x < 999:
    imageName = ""
    imageName = str("./img_" + str(x) + ".jpg")
    camera.capture(imageName)
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                print("stop")
                x+=1
