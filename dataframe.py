import os
import scipy.io
import pandas as pd

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
    mat = scipy.io.loadmat(mat_file)
    impedance = mat['Zc']
    frequency = mat['freq']
    
    # Create a list of dictionaries containing the data
    for i in range(len(frequency)):
        data.append({
            'h': h,
            'g': g,
            'w': w,
            'd': d,
            'turns': turns,
            'frequency': frequency[i][0],
            'impedance': impedance[i][0]
        })

# Create a pandas DataFrame from the data
df = pd.DataFrame(data)

# Print the resulting DataFrame
print(df)

