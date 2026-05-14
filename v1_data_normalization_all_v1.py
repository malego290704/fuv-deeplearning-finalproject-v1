import glob
import os
import tqdm
# Assuming your function is in a file named process_script.py
from v1_data_normalization_v3 import process_stock_data 

source_folder = './v1-data'
output_folder = './v1-data-normalized'

os.makedirs(output_folder, exist_ok=True)

# glob returns the full path: './v1-data/MSFT-NASDAQ.csv'
filenames = glob.glob(f"{source_folder}/*.csv")

for filename in tqdm.tqdm(filenames):
    # os.path.basename(filename) gives: 'MSFT-NASDAQ.csv'
    file_name_with_ext = os.path.basename(filename)
    
    # Construct the full output path: './v1-data-ready/MSFT-NASDAQ.csv'
    output_path = os.path.join(output_folder, file_name_with_ext)
    
    # Run the function
    process_stock_data(filename, output_path)

print("Batch processing complete.")