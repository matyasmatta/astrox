import pandas as pd
import glob
import os
import csv

def merge_csv_files(csv_folder, output_file):
    for files in os.listdir(csv_folder):
        with open(csv_folder + "/" + files, 'r', newline='') as f:
            reader = csv.reader(f)
            header = str(files)
            for row in reader:
                shadow_output = row[0]
                shadow_lenght_avg_px = row[1]
                shadow_lenght_mm_px  = row[2]
                shadow_lenght_md_px = row[3]
                diff = row[4]
                with open(output_file, "a", newline='') as f2:
                    writer = csv.writer(f2)
                    row_print = header, shadow_output, shadow_lenght_avg_px, shadow_lenght_mm_px, shadow_lenght_md_px, diff
                    writer.writerow(row_print)

# Specify the folder containing the CSV files and the output file path
csv_folder = r'E:\absolute_final\ai_output_csv'
output_file = r'C:\Users\kiv\Documents\GitHub\astrox\maty\merge63.csv'

# Merge CSV files
merge_csv_files(csv_folder, output_file)
