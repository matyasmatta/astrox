from picamera import PiCamera
from time import sleep

camera = PiCamera()
camera.rotation = 180

camera.start_preview()
sleep(40)
camera.annotate_text = "Chus!"
camera.image_effect = 'negative'
camera.capture('./negativ.jpg')
camera.stop_preview()
print("Je to tam!")    
# test
# checking for experimental branch