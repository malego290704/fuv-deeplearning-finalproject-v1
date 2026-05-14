import datetime
import csv
import tqdm

def process(fileinp: str=None, fileout: str=None, verbose: bool=False) -> int:
    if fileinp == None or fileinp == '':
        return -1
    epoch = datetime.date(1970, 1, 1)
    csvdata = []
    with open(fileinp, 'r', newline='', encoding='utf-8') as csvfile:
        dictreader = csv.DictReader(csvfile)
        for row in tqdm.tqdm(dictreader, disable=(not verbose), desc='Reading...'):
            csvdata.append(row)
    outputdata: list[dict] = []
    for rowdata in tqdm.tqdm(csvdata, disable=(not verbose), desc='Processing...'):
        row = {}
        row['low'] = rowdata['Low']
        row['high'] = rowdata['High']
        row['open'] = rowdata['Open']
        row['close'] = rowdata['Close']
        row['volume'] = rowdata['Volume']
        date = rowdata['Date']
        try:
            dateo = datetime.datetime.strptime(date, '%d-%m-%Y').date()
        except ValueError as e:
            raise ValueError(f'Invalid time data for {fileinp}: {e}')
        row['year'] = dateo.year
        row['month'] = dateo.month
        row['day'] = dateo.day
        row['weekday'] = dateo.isoweekday()
        row['days'] = (dateo - epoch).days
        outputdata.append(row)
    if fileout == None or fileout == '':
        print(outputdata[:5])
        return len(outputdata)
    with open(fileout, 'w', newline='', encoding='utf-8') as csvfile:
        dictwriter = csv.DictWriter(csvfile, fieldnames=outputdata[0].keys())
        dictwriter.writeheader()
        dictwriter.writerows(outputdata)
    return len(outputdata)

if __name__ == '__main__':
    process('raw-data/csv/AAPL.csv', 'v1-processed-AAPL-NASDAQ.csv', verbose=True)