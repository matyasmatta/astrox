import yolov8_lib
import shadow
path = r'C:\Users\kiv\Downloads\AstroX\chops\corrected_img_21_3.jpg'
ai_output = yolov8_lib.get_results(path = path, name='corrected_img_21_3.jpg')
exif = 

for i in range(len(ai_output)):
    angle = 350
    shadow_output = shadow.calculate_shadow(x=ai_output[i]['xcentre'], y=ai_output[i]['ycentre'],file_path=path, angle = angle)