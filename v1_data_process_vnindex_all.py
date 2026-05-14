import glob
import json
import v1_data_process_vn_single_v4 as v1vn_single
import tqdm

filenames = glob.glob("./raw-data/stock-historical-data/*-VNINDEX-History.csv")

folderoutname = './v1-data'

company_names = []

index_data = []

for filename in tqdm.tqdm(filenames):
    company_name = filename[33:-20]
    company_names.append(company_name)
    fileoutname = f'{company_name}-VNINDEX.csv'
    datalen = v1vn_single.process(filename, f'{folderoutname}/{fileoutname}')
    index_data.append({
        'ticker': company_name,
        'filename': fileoutname,
        'length': datalen
    })

with open(f'{folderoutname}/indexes/index-vnindex.json', "w") as f:
    json.dump(index_data, f, indent=4)