from ultralytics import YOLO
import cv2
from PIL import ImageDraw
from PIL import Image
import os


def resize_image(img, scale_percent) :
    # Calculate new size
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    # Resize image
    resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    return resized

def draw_box(img, result, class_list) :
    # Get information from result
    xyxy= result.boxes.xyxy.numpy()
    
    confidence= result.boxes.conf.numpy()
    class_id= result.boxes.cls.numpy().astype(int)
    # Get Class name
    class_name = [class_list[x] for x in class_id]
    # Pack together for easy use
    sum_output = list(zip(class_name, confidence,xyxy))
    # Copy image, in case that we need original image for something
    out_image = img.copy()
    for run_output in sum_output :
        # Unpack
        label, con, box = run_output
        # Choose color
        box_color = (0, 0, 255)
        text_color = (255,255,255)
        # Draw object box
        first_half_box = (int(box[0]),int(box[1]))
        second_half_box = (int(box[2]),int(box[3]))
        cv2.rectangle(out_image, first_half_box, second_half_box, box_color, 1)
        # Create text
        text_print = '{label} {con:.2f}'.format(label = label, con = con)
        # Locate text position
        text_location = (int(box[0]), int(box[1] - 10 ))
        # Get size and baseline
        labelSize, baseLine = cv2.getTextSize(text_print, cv2.FONT_HERSHEY_SIMPLEX, 1, 1) 
        # Draw text's background
        cv2.rectangle(out_image 
                        , (int(box[0]), int(box[1] - labelSize[1] - 10 ))
                        , (int(box[0])+labelSize[0], int(box[1] + baseLine-10))
                        , box_color , cv2.FILLED) 
        # Put text
        cv2.putText(out_image, text_print ,text_location
                    , cv2.FONT_HERSHEY_SIMPLEX ,1
                    , text_color, 2 ,cv2.LINE_AA)
    return out_image

def get_results(result, path, name):
    xyxy= result[0].boxes.data.numpy()
    i_for_search = 0
    i_for_photos = 0
    bbox = {}
    ai_output = {}
    image = Image.open(path)
    draw = ImageDraw.Draw(image)
    skipped = 0
    try:
        for obj in xyxy:
            ai_output[i_for_search] = {}
            bbox['xmin'] = int(round(xyxy[i_for_search][0]))
            bbox['xmax'] = int(round(xyxy[i_for_search][2]))
            bbox['ymin'] = int(round(xyxy[i_for_search][1]))
            bbox['ymax'] = int(round(xyxy[i_for_search][3]))
            bbox['accuracy'] = xyxy[i_for_search][4]
            print(bbox)

            x_centre = (bbox['xmin']+bbox['xmax'])/2
            y_centre = (bbox['ymin']+bbox['ymax'])/2
            
            x_check = []
            for counter in range(20):
                x_check.append(x_centre+counter-10)
            resemble = False
            
            for sub_counter in range(i_for_photos-1):
                try:
                    for element in x_check:
                        try:
                            element = int(round(element)) 
                            if element == ai_output[sub_counter]['xcentre']:
                                resemble = True
                                break
                        except:
                            pass
                except:
                    pass

            if resemble:
                print("true")

            width = bbox['xmax']-bbox['xmin']
            if bbox['accuracy'] > 0.6 and resemble == False and width < 100:
                draw.rectangle([bbox['xmin'], bbox['ymin'], bbox['xmax'], bbox['ymax']], outline='red')
                draw.text((bbox['xmin'] + 10, bbox['ymin'] + 10), text = str(i_for_photos), fill='red')

                ai_output[i_for_photos]['xmin'] = int(round(xyxy[i_for_search][0]))
                ai_output[i_for_photos]['xmax'] = int(round(xyxy[i_for_search][2]))
                ai_output[i_for_photos]['ymin'] = int(round(xyxy[i_for_search][1]))
                ai_output[i_for_photos]['ymax'] = int(round(xyxy[i_for_search][3]))
                ai_output[i_for_photos]['xcentre'] = int((bbox['xmin']+bbox['xmax'])/2)
                ai_output[i_for_photos]['ycentre'] = int((bbox['ymin']+bbox['ymax'])/2)
                ai_output[i_for_photos]['accuracy'] = xyxy[i_for_search][4]
                i_for_photos += 1
            else:
                skipped += 1
            i_for_search += 1

    except:
        pass
    image.save(r'C:\Users\kiv\Downloads\AstroX\meta_yolo_3/meta_' + name +'.bmp')
    print(skipped)

# Load a model
model = YOLO("yolov8_latest.pt")  # load a pretrained model (recommended for training)
class_list = model.model.names
scale_show = 100
for file_name in os.listdir(r'C:\Users\kiv\Downloads\AstroX\chops'):
    file_path = r'C:\Users\kiv\Downloads\AstroX\chops/'+ file_name
    results = model(file_path)  # predict on an image
    img = cv2.imread(file_path)
    labeled_img = draw_box(img, results[0], class_list)
    display_img = resize_image(labeled_img, scale_show)
    get_results(results, file_path, file_name)