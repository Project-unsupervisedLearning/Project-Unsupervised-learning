import nd2
import os
import numpy as np
import pandas as pd

def extract_features(ndfile):
    values = ndfile.asarray()
    channels = [channel.channel.name for channel in ndfile.metadata.channels]
    exposure_time = extractexpos(ndfile)  # Adjust based on actual structure if necessary
    
    data = {}
    for i, channel in enumerate(channels):
        matrix = values[i]
        std = matrix.std()
        mean = matrix.mean()
        
        match channel:
            case "Intensity":
                matrix = matrix * (1000 / exposure_time)
                std = matrix.std()
                mean = matrix.mean()
                data[f"{channel} Std"] = std
                data[f"{channel} Mean"] = mean
            case "Phase":
                data[f"{channel} Std"] = std
                data[f"{channel} Mean"] = mean
            case "Modulation":
                data[f"{channel} Std"] = std
                data[f"{channel} Mean"] = mean
            case "Phase Lifetime":
                data[f"{channel} Std"] = std
                data[f"{channel} Mean"] = mean
            case "Modulation Lifetime":
                data[f"{channel} Std"] = std
                data[f"{channel} Mean"] = mean
            case _:
                print(f"Unknown channel: {channel}")
    
    return data

def extractexpos(ndfile):
    text_info = ndfile.text_info['capturing']
    exposure_time_str = None
    
    for line in text_info.split('\r\n'):
        if 'Exposure: ' in line:
            exposure_time_str = line.split('Exposure: ')[1].split(' ')[0]
            break
    
    if exposure_time_str is None:
        raise ValueError("Exposure time not found in metadata.")
    
    try:
        exposure_time = float(exposure_time_str)
    except ValueError:
        raise ValueError(f"Could not convert exposure time to float: {exposure_time_str}")
    
    return exposure_time

src_dir = r'E:\PROJECT'  # Directory containing .nd2 files

all_features = []

for root, dirs, files in os.walk(src_dir):
    for filename in files:
        if filename.endswith(".nd2"):
            src = os.path.join(root, filename)
            with nd2.ND2File(src) as ndfile:
                features = extract_features(ndfile)
                features['Filename'] = filename  # Add the filename to the features
                all_features.append(features)


# Convert the list of dictionaries to a pandas DataFrame
df = pd.DataFrame(all_features)
df.set_index('Filename', inplace=True)
df.to_csv('FOOD.csv', index=False)
