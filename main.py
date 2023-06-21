# NOTE: This is not the code that ran on the ISS, it's the post-processing main, that is available under branch "release"
# Import libraries, many of them are our own
import yolov8_lib
import shadow_lib
import exifmeta
import north_lib
import os
import re
import json 
import numpy as np
import csv

# Initialise variables
file = list()
i = int()

# Create run folder (so that it can be ran multiple times)
global run_path
folder_path = r"C:\Users\kiv\Downloads\AstroX\runs/" # Specify the path
subfolders = [name for name in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, name))]
run_count = len(subfolders) + 1
run_path = (folder_path + str(run_count))
os.mkdir(run_path)
os.mkdir(run_path+"/meta_ai")
os.mkdir(run_path+"/meta_shadow")
os.mkdir(run_path+"/ai_output_json")
os.mkdir(run_path+"/ai_output_csv")
os.mkdir(run_path+"/pixel_txt")
os.mkdir(run_path+"/pixel_graph")
del folder_path, i, file, run_count

# Specify where chops are saved (source data)
folder_path = r'C:\Users\kiv\Downloads\AstroX\chops'
for files in os.listdir(folder_path):

    # Get data from AI library
    path = folder_path + "/" + files
    ai_output = yolov8_lib.get_results(path = path, name=files, run_path=run_path)
    ai_output = {k: v for k, v in ai_output.items() if v} # Empty items are created, hence need to be removed
    
    # Get north from north library
    path2 = r'C:\Users\kiv\Downloads\AstroX\chops' + "/" + files[0:14] + str(int(re.findall(r'\d+', files)[0]) + 1) + files[-6:]
    north = north_lib.find_north_fast(path, path2)

    # Get Sun azimuth and shadow angle from metadata
    year, month, day, hour, minute, second = exifmeta.find_time(path)
    azimuth = exifmeta.sun_data.azimuth(exifmeta.get_latitude(path), exifmeta.get_longitude(path), year, month, day, hour, minute, second)
    angle = (north + azimuth + 180) % 360

    # Run for all shadows on chop
    for i in range(len(ai_output)):
        
        # Get shadow data from shadow library
        try: shadow_output, shadow_lenght_avg_px, shadow_lenght_mm_px, shadow_lenght_md_px, diff = shadow_lib.calculate_shadow(x=ai_output[i]['xcentre'], y=ai_output[i]['ycentre'],file_path=path, angle = angle, run_path = run_path, 
        file_name = files, cloud_id=i, image_id = files)
        except: shadow_output = shadow_lenght_avg_px = shadow_lenght_mm_px =  shadow_lenght_md_px = diff = "Error was raised properly"
        
        # Import all data into ai_output dictionary
        ai_output[i]["cloud_height_m"] = shadow_output
        ai_output[i]["shadow_lenght_px"] = shadow_lenght_avg_px
        ai_output[i]["north_deg"] = north
        ai_output[i]["azimuth_deg"] = azimuth
        ai_output[i]["angle_deg"] = angle
        ai_output[i]["shadow_lenght_mm_px"] = shadow_lenght_mm_px
        ai_output[i]["shadow_lenght_md_px"] = shadow_lenght_md_px
        ai_output[i]["diff"] = diff

        # Import the dictionary items into CSV, where CSVs are also created progressively
        with open(run_path + "/ai_output_csv/ai_output_" + files +".csv", "a", newline='') as outfile:
            csv_writer = csv.writer(outfile)
            csv_writer.writerow([shadow_output, shadow_lenght_avg_px, shadow_lenght_mm_px, shadow_lenght_md_px, diff])
    
    # Dump the whole dictionary into JSON, as it needs no conversion, JSONs are created progressively
    with open(run_path + "/ai_output_json/ai_output_" + files +".json", "w") as outfile:
        json.dump(ai_output, outfile, indent=4, default=lambda x: x.tolist() if isinstance(x, np.ndarray) else str(x))
    
    