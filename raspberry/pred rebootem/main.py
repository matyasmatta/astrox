from picamera import PiCamera
from time import sleep

camera = PiCamera()

camera.start_preview()
sleep(100)
camera.annotate_text = "Chus!"
camera.image_effect = 'negative'
camera.capture('./negativ.jpg')
camera.stop_preview()
print("Je to tam!")
Naruto = True
if Naruto:
    print("Datebajo!")      
# test
# checking for experimental branch2