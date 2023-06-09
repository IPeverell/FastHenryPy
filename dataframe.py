import os
import scipy.io
import pandas as pd
import re
import numpy as np
import altair as alt

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

#correct data types
df.turns = pd.to_numeric(df.turns)
df.g = pd.to_numeric(df.g)
df.h = pd.to_numeric(df.h)
df.w = pd.to_numeric(df.w)

# Print the resulting DataFrame to csv
#df.to_csv('Zc.csv', index=False)
df['imped_r'] = np.real(df.impedance)
df['imped_i'] = np.imag(df.impedance)
df = df.drop(['impedance'],axis=1)

#Sieve data
df = df.loc[df['frequency'] == 1.4678e7]
#df = df.loc[df['h']==0.1]
df = df.loc[df['g'] == 0.1]
df = df.loc[df['w']==0.1]
#df = df.loc[df['turns']==1]

print(df)
#Visualise the dataframe
alt.renderers.enable('altair_viewer')

# make the chart
chart = alt.Chart(df).mark_point().encode(
    x='imped_r',
    y='imped_i'
)

chart = chart + chart.transform_regression('imped_r','imped_i').mark_line()
chart.interactive().show()





