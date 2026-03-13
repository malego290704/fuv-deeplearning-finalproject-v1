import pandas as pd

def process(fileinp: str, fileout: str) -> int:
    # Read CSV
    df = pd.read_csv(fileinp)
    
    # Convert date column once (vectorized)
    df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y')
    
    # Vectorized extraction (very fast)
    df['year'] = df['Date'].dt.year
    df['month'] = df['Date'].dt.month
    df['day'] = df['Date'].dt.day
    df['weekday'] = df['Date'].dt.weekday + 1
    df['days'] = (df['Date'] - pd.Timestamp('1970-01-01')).dt.days
    
    # Rename original columns to match your lowercase requirement
    df = df.rename(columns={
        'Low': 'low', 'High': 'high', 'Open': 'open', 
        'Close': 'close', 'Volume': 'volume'
    })
    
    # Select only the columns you want
    cols = ['low', 'high', 'open', 'close', 'volume', 'year', 'month', 'day', 'weekday', 'days']
    df[cols].to_csv(fileout, index=False)
    
    return len(df)



if __name__ == '__main__':
    process('raw-data/csv/AAPL.csv', 'v1-processed-AAPL-NASDAQ.csv')