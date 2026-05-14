import datetime
import csv
import tqdm

def process(fileinp: str, fileout: str, verbose: bool = False) -> int:
    epoch = datetime.date(1970, 1, 1)
    count = 0

    with open(fileinp, 'r', encoding='utf-8') as f_in, \
         open(fileout, 'w', newline='', encoding='utf-8') as f_out:
        
        reader = csv.DictReader(f_in)
        writer = None
        
        # tqdm logic
        pbar = tqdm.tqdm(disable=not verbose, desc='Processing...')

        for rowdata in reader:
            # OPTIMIZATION: String splitting/slicing is much faster than strptime
            d, m, y = map(int, rowdata['Date'].split('-'))
            dateo = datetime.date(y, m, d)
            
            # Map values directly
            row = {
                'low': rowdata['Low'],
                'high': rowdata['High'],
                'open': rowdata['Open'],
                'close': rowdata['Close'],
                'volume': rowdata['Volume'],
                'year': y,
                'month': m,
                'day': d,
                'weekday': dateo.isoweekday(),
                'days': (dateo - epoch).days
            }

            if writer is None:
                writer = csv.DictWriter(f_out, fieldnames=row.keys())
                writer.writeheader()
            
            writer.writerow(row)
            count += 1
            if verbose: pbar.update(1)
            
        if verbose: pbar.close()
    return count



if __name__ == '__main__':
    process('raw-data/csv/AAPL.csv', 'v1-processed-AAPL-NASDAQ.csv', verbose=True)