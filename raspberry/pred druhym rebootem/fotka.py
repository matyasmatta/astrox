from picamera import PiCamera
from time import sleep

camera = PiCamera()


camera.start_preview()
sleep(5)
camera.capture('/home/admin/Desktop/image.jpg')
camera.stop_preview()
camera.rotation = 180
camera.start_preview()
sleep(5)
camera.capture('/home/admin/Desktop/image1.jpg')
camera.stop_preview()
