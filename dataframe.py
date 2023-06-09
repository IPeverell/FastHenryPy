import os
import scipy.io
import pandas as pd
import re
import numpy as np

def read_Zc(path):
    # Read the text file
    with open(path, "r") as file:
        file_contents = file.read()
    
    # Extract frequency and impedance values using regular expressions
    pattern = r"Impedance matrix for frequency = (\d+(?:\.\d+)?(?:[eE][-+]?\d+)?) \d+ x \d+\n\s+([\d.]+)\s+\+([\d.]+)j"
    matches = re.findall(pattern, file_contents)
    
    # Create numpy arrays for frequency and impedance values
    frequencies = np.array([float(match[0]) for match in matches])
    impedances_real = np.array([float(match[1]) for match in matches])
    impedances_imaginary = np.array([float(match[2]) for match in matches])
    impedances = impedances_real + 1j * impedances_imaginary
    
    # Print the numpy array
    print("Frequencies:", frequencies)
    print("Impedances:", impedances)
    return frequencies,impedances
# Initialize empty lists to store data
data = []

# Iterate over folders in the current directory
for folder_name in os.listdir('.'):
    if not os.path.isdir(folder_name):
        continue  # Skip non-directory files
    
    # Extract variables from folder name
    h, g, w, d, turns = folder_name.split(',')
    
    # Path to Zc.mat file
    mat_file = os.path.join(folder_name, 'Zc.mat')
    
    if not os.path.isfile(mat_file):
        continue  # Skip if Zc.mat file does not exist
    
    # Load impedance data from Zc.mat file
    frequency,impedance = read_Zc(mat_file)
    
    # Create a list of dictionaries containing the data
    for i in range(len(frequency)):
        data.append({
            'h': h,
            'g': g,
            'w': w,
            'd': d,
            'turns': turns,
            'frequency': frequency[i],
            'impedance': impedance[i]
        })

# Create a pandas DataFrame from the data
df = pd.DataFrame(data)

# Print the resulting DataFrame
print(df)

