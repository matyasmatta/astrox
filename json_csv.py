import json
import csv
import os

import json
import os
import pandas as pd

def merge_jsons(json_dir, output_file):
    merged_data = {}

    for json_file in os.listdir(json_dir):
        if json_file.endswith('.json'):
            json_path = os.path.join(json_dir, json_file)
            with open(json_path) as f:
                data = json.load(f)

            json_name = os.path.splitext(json_file)[0]
            merged_data[json_name] = data

    with open(output_file, 'w') as f:
        json.dump(merged_data, f, indent=4)

def json_to_csv(json_file, csv_file):
    with open(json_file) as f:
        data = json.load(f)

    # If the JSON contains a single object, wrap it in a list
    if isinstance(data, dict):
        data = [data]

    # Use pandas to convert JSON to DataFrame
    df = pd.json_normalize(data)

    # Save DataFrame to CSV
    df.to_csv(csv_file, index=False)


# Specify the input JSON file and output CSV file paths
json_file = r'C:\Users\kiv\Downloads\AstroX\runs\58\experimental_csv/merged.json'
csv_file = r'C:\Users\kiv\Downloads\AstroX\runs\58\experimental_csv/merged.csv'

# Convert JSON to CSV
json_to_csv(json_file, csv_file)