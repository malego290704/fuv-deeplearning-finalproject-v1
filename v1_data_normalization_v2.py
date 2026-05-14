import polars as pl
import numpy as np
from datetime import datetime

# Constants
YEAR_MIN, YEAR_MAX = 1970, 2030
EPOCH_START = datetime(1970, 1, 1)
EPOCH_END = datetime(2030, 12, 31)
TOTAL_DAYS_LIMIT = (EPOCH_END - EPOCH_START).days 

def process_stock_data(input_file, output_file):
    df = pl.scan_csv(input_file)

    log_cols = ['low', 'high', 'open', 'close', 'volume']

    processed_df = (
        df
        # 1. Log Returns
        .with_columns([
            (pl.col(col) / pl.col(col).shift(1)).log().alias(col)
            for col in log_cols
        ])
        .drop_nulls()
        
        # 2. Linear Normalization
        .with_columns([
            ((pl.col("year") - YEAR_MIN) / (YEAR_MAX - YEAR_MIN)).alias("year"),
            (pl.col("days") / TOTAL_DAYS_LIMIT).alias("days")
        ])
        
        # 3. Cyclical Encoding (Using your 1-based start)
        .with_columns([
            # Month: 1 to 12. Divisor 12.
            (pl.col("month").cast(pl.Float64) * 2 * np.pi / 12).sin().alias("month_sin"),
            (pl.col("month").cast(pl.Float64) * 2 * np.pi / 12).cos().alias("month_cos"),
            
            # Day: 1 to 31. Divisor 31.
            (pl.col("day").cast(pl.Float64) * 2 * np.pi / 31).sin().alias("day_sin"),
            (pl.col("day").cast(pl.Float64) * 2 * np.pi / 31).cos().alias("day_cos"),
            
            # Weekday: 1 to 7 (Mon=1, Sun=7). Divisor 7.
            (pl.col("weekday").cast(pl.Float64) * 2 * np.pi / 7).sin().alias("weekday_sin"),
            (pl.col("weekday").cast(pl.Float64) * 2 * np.pi / 7).cos().alias("weekday_cos"),
        ])
        .drop(["month", "day", "weekday"])
    )

    processed_df.collect().write_csv(output_file)

process_stock_data('./v1-data/MSFT-NASDAQ.csv', './v1-data-ready/MSFT-NASDAQ.csv')