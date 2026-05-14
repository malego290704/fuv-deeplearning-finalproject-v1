import json
import csv

full_index = []

folder = './v1-data/indexes'
exchanges = ['nasdaq', 'vnindex', 'hnxindex', 'upcomindex']
for exchange in exchanges:
    file_name = f'{folder}/index-{exchange}.json'
    try:
        with open(file_name, 'r') as f:
            partial_index = json.load(f)
            for item in partial_index:
                item['exchange'] = exchange
            full_index.extend(partial_index)
    except FileNotFoundError:
        print(f"Warning: {file_name} not found.")
    except json.JSONDecodeError:
        print(f"Error: {file_name} is not a valid JSON file.")

with open(f'{folder}/index.json', 'w') as f:
    json.dump(full_index, f, indent=4)

with open(f'{folder}/index.csv', 'w', newline='', encoding='utf-8') as csvfile:
    dictwriter = csv.DictWriter(csvfile, fieldnames=['ticker', 'exchange', 'filename', 'length'])
    dictwriter.writeheader()
    dictwriter.writerows(full_index)