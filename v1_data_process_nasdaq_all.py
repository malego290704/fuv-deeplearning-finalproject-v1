import glob
import json
import v1_data_process_nasdaq_single_v4 as v1nasdaq_single
import tqdm

filenames = glob.glob("./raw-data/csv/*.csv")

folderoutname = './v1-data'

company_names = []

index_data = []

for filename in tqdm.tqdm(filenames):
    company_name = filename[15:-4]
    company_names.append(company_name)
    fileoutname = f'{company_name}-NASDAQ.csv'
    datalen = v1nasdaq_single.process(filename, f'{folderoutname}/{fileoutname}')
    index_data.append({
        'ticker': company_name,
        'filename': fileoutname,
        'length': datalen
    })

with open(f'{folderoutname}/indexes/index-nasdaq.json', "w") as f:
    json.dump(index_data, f, indent=4)