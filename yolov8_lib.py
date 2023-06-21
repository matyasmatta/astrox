from ultralytics import YOLO
import cv2
from PIL import ImageDraw
from PIL import Image
import os

# Function for OpenCV resizing
def resize_image(img, scale_percent) :
    # Calculate new size
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    # Resize image
    resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    return resized

# Function for BBoxes via OpenCV (legacy)
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

# Main run function
def get_results(path, name, run_path = "./"):
    
    # configuration (migrated from main())
    model = YOLO("yolov8_latest.pt")
    class_list = model.model.names
    scale_show = 100
    results = model(path) 
    img = cv2.imread(path)
    img = resize_image(img, 200)

    xyxy= results[0].boxes.data.numpy()
    i_for_search = 0
    i_for_photos = 0
    bbox = {}
    ai_output = {}
    image = Image.open(path)
    draw = ImageDraw.Draw(image)
    skipped = 0
    try:
        for obj in xyxy:
            # Dump data into BBOX dict
            ai_output[i_for_search] = {}
            bbox['xmin'] = int(round(xyxy[i_for_search][0]))
            bbox['xmax'] = int(round(xyxy[i_for_search][2]))
            bbox['ymin'] = int(round(xyxy[i_for_search][1]))
            bbox['ymax'] = int(round(xyxy[i_for_search][3]))
            bbox['accuracy'] = xyxy[i_for_search][4]
            print(bbox)

            # Calculate centre for each data coordinate
            centre = {}
            centre['x'] = (bbox['xmin']+bbox['xmax'])/2
            centre['y'] = (bbox['ymin']+bbox['ymax'])/2

            # Below is a complex algorithm that works to remove overlapping BBoxes (YOLOv8 does not have default); also called non-max-suppresion
            resemble_x = False
            resemble_y = False

            # Checks the already existing ai_output dict if there is a centre similar to this one already
            def check(a):
                if a == "x":
                    centre_var = "xcentre"
                else:
                    centre_var = "ycentre"
                check = []
                for counter in range(16):
                    check.append(centre[a]+counter-8)
                resemble = False
                for sub_counter in range(i_for_photos-1):
                    try:
                        for element in check:
                            try:
                                element = int(round(element)) 
                                if element == int(round(ai_output[sub_counter+1][centre_var])):
                                    resemble = True
                                    break
                            except:
                                pass
                    except:
                        pass
                return resemble
            
            # Check for both x and y
            resemble_x = check('x')
            resemble_y = check('y')

            # Add data to ai_output dict after validation; conditions specified below; we settled on 65 percent accuracy
            width = bbox['xmax']-bbox['xmin']
            if bbox['accuracy'] > 0.65 and resemble_x == False and resemble_y == False and width < 100:
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
    image.save(run_path +"/meta_ai/meta" + name +'.bmp')
    return ai_output