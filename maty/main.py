import yolov8_lib
import shadow_lib
import exifmeta
import north_lib
import os
import re
import json 
import numpy as np

# initialise the save folder
file = list()
i = int()

global run_path
folder_path = r"C:\Users\kiv\Downloads\AstroX\runs/"
subfolders = [name for name in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, name))]
run_count = len(subfolders) + 1
run_path = (folder_path + str(run_count))
os.mkdir(run_path)
os.mkdir(run_path+"/meta_ai")
os.mkdir(run_path+"/meta_shadow")
os.mkdir(run_path+"/ai_output")
del folder_path, i, file, run_count

folder_path = r'C:\Users\kiv\Downloads\AstroX\chops'
for files in os.listdir(folder_path):

    path = folder_path + "/" + files
    ai_output = yolov8_lib.get_results(path = path, name=files, run_path=run_path)
    ai_output = {k: v for k, v in ai_output.items() if v} # Empty items are created, hence need to be removed

    path2 = folder_path + "/" + files[0:14] + str(int(re.findall(r'\d+', files)[0]) + 1) + files[-6:]
    north = north_lib.find_north_fast(path, path2)
    year, month, day, hour, minute, second = exifmeta.find_time(path)
    azimuth = exifmeta.sun_data.azimuth(exifmeta.get_latitude(path), exifmeta.get_longitude(path), year, month, day, hour, minute, second)
    angle = (north + azimuth + 180) % 360
    for i in range(len(ai_output)):
        shadow_output = shadow_lib.calculate_shadow(x=ai_output[i]['xcentre'], y=ai_output[i]['ycentre'],file_path=path, angle = angle, run_path = run_path, file_name = files)
        ai_output[i]["shadow_lenght"] = shadow_output
    with open(run_path + "/ai_output/ai_output_" + files +".json", "w") as outfile:
        json.dump(ai_output, outfile, indent=4, default=lambda x: x.tolist() if isinstance(x, np.ndarray) else str(x))
    