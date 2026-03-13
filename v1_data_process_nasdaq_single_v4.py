import polars as pl

def process(fileinp: str, fileout: str):
    # Scan the CSV (lazy evaluation)
    df = (
        pl.scan_csv(fileinp)
        .with_columns(
            # 1. Convert string to Date type
            pl.col("Date").str.to_date("%d-%m-%Y")
        )
        .with_columns([
            # 2. Extract components
            pl.col("Date").dt.year().alias("year"),
            pl.col("Date").dt.month().alias("month"),
            pl.col("Date").dt.day().alias("day"),
            pl.col("Date").dt.weekday().alias("weekday"),
            
            # 3. Use to_physical() to get days since 1970-01-01 directly
            pl.col("Date").to_physical().alias("days")
        ])
        .rename({
            "Low": "low", "High": "high", "Open": "open", 
            "Close": "close", "Volume": "volume"
        })
        # 4. Select columns in the order you want
        .select([
            'low', 'high', 'open', 'close', 'volume', 
            'year', 'month', 'day', 'weekday', 'days'
        ])
        .collect() # Execute all operations
    )
    
    df.write_csv(fileout)
    return len(df)

if __name__ == '__main__':
    process('raw-data/csv/AAPL.csv', 'v1-processed-AAPL-NASDAQ.csv')