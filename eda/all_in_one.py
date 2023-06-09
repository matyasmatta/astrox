import cv2
import numpy as np
from PIL import Image
import os
from os import listdir


def copy_exif_data(source_image, target_image):
    with Image.open(source_image) as source:
        with Image.open(target_image) as target:
            exif_data = source.info.get('exif')
            target.save(target_image, exif=exif_data)

def adjust_perspektive_one_image(path_to_image_from_ISS, path_to_image_perspective, number_of_image_in_perspektive):
    frame = cv2.imread(path_to_image_from_ISS)
    # Locate points of the documents
    # or object which you want to transform
    pts1 = np.float32([[0, 0], [4056, 0], [54, 3040], [3638, 3040]])
    pts2 = np.float32([[0, 0], [4056, 0], [0, 3040], [4056, 3040]])
        
    # Apply Perspective Transform Algorithm
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    result = cv2.warpPerspective(frame, matrix, (4056, 3040))


    cv2.imwrite(path_to_image_perspective, result)

    copy_exif_data(path_to_image_from_ISS, path_to_image_perspective)
    '''
    # load new image
    dsize = (812, 606)
    frame = cv2.resize(frame, dsize)
    result = cv2.resize(result, dsize)
    while True:
        # Wrap the transformed image
        cv2.imshow('frame', frame) # Initial Capture
        cv2.imshow('frame1', result) # Transformed Capture
        if cv2.waitKey(24) == 27:
            break
    cv2.destroyAllWindows()
    '''
    print('number_of_image_in_perspektive:',number_of_image_in_perspektive)

def adjust_perspektive_massively(path_to_folder_from_ISS, path_to_folder_perspective):
    number_of_image_in_perspektive = 0
    while True:
        try:
            path_to_image_from_ISS = path_to_folder_from_ISS+"img_"+str(number_of_image_in_perspektive)+".jpg" 
            path_to_image_perspective = path_to_folder_perspective+'img_'+str(number_of_image_in_perspektive)+'.jpg'
            adjust_perspektive_one_image(path_to_image_from_ISS,path_to_image_perspective,number_of_image_in_perspektive)
            number_of_image_in_perspektive+=1
        except:
            break

def get_middle(path_to_folder_perspective, path_to_folder_middle):
    # get the path or directory
    for images in os.listdir(path_to_folder_perspective):
        # check if the image ends with png or jpg or jpeg
        if (images.endswith(".png") or images.endswith(".jpg")\
            or images.endswith(".jpeg")):
            # display
            print(images)
            # Opens a image in RGB mode
            im = Image.open(path_to_folder_perspective+ images)
            left = 1515
            top = 505
            right = 2525
            bottom = 1515
            # Cropped image of above dimension
            # (It will not change original image)
            im1 = im.crop((left, top, right, bottom))
            #Metadata
            exif = im.info['exif']

            # Shows the image in image viewer
            im1.save(path_to_folder_middle+images,exif=exif)

def make_4_chops(path_to_folder_middle, path_to_folder_chops):
    for images in os.listdir(path_to_folder_middle):
        # check if the image ends with png or jpg or jpeg
        if (images.endswith(".png") or images.endswith(".jpg")\
            or images.endswith(".jpeg")):
            # display
            print(images)
            # Opens a image in RGB mode
            im = Image.open(path_to_folder_middle + images)
            # Slice
            infile = path_to_folder_middle+images
            chopsize = 505

            img = Image.open(infile)
            width, height = img.size

            # Metadata
            exif = im.info['exif']
            images = images.split(sep='.jpg')

            # Save Chops of original image
            number_of_chop = 1
            for y0 in range(0, height, chopsize):
                for x0 in range(0, width, chopsize):
                    box = (x0, y0,
                            x0+chopsize if x0+chopsize <  width else  width - 1,
                            y0+chopsize if y0+chopsize < height else height - 1)
                    print('%s %s' % (infile, box))
                    idk= number_of_chop
                    images_path = path_to_folder_chops + images[0] +'_'+ str(number_of_chop) + ".jpg"
    #                if ((x0 == 2020 or x0 == 1515) and (y0 == 505 or y0 == 1010 or y0 == 1515)):
                    img.crop(box).save(images_path,exif=exif)
                    number_of_chop+=1

def all_in_one(path_to_folder_from_ISS, path_to_folder_perspective, path_to_folder_middle, path_to_folder_chops):
    adjust_perspektive_massively(path_to_folder_from_ISS,path_to_folder_perspective)
    get_middle(path_to_folder_perspective,path_to_folder_middle)
    make_4_chops(path_to_folder_middle, path_to_folder_chops)


path_to_folder_from_ISS = "./from_ISS/"
path_to_folder_perspective = './perspective_adjustment/'
path_to_folder_middle = './middle/'
path_to_folder_chops = './chops/'
all_in_one(path_to_folder_from_ISS, path_to_folder_perspective, path_to_folder_middle, path_to_folder_chops)





