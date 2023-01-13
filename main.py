from picamera import PiCamera
from time import sleep

camera = PiCamera()
camera = PiCamera()
camera.rotation = 180

camera.start_preview()
sleep(5)
camera.annotate_text = "Čus!"
camera.image_effect = 'negative'
camera.capture('/home/pi/Desktop/negativ.jpg')
camera.stop_preview()

# test