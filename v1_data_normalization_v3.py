import polars as pl
import numpy as np
from datetime import datetime

# Constants
YEAR_MIN, YEAR_MAX = 1970, 2030
EPOCH_START = datetime(1970, 1, 1)
EPOCH_END = datetime(2030, 12, 31)
TOTAL_DAYS_LIMIT = (EPOCH_END - EPOCH_START).days 

def process_stock_data(input_file, output_file):
    log_cols = ['low', 'high', 'open', 'close', 'volume']

    df = (
        pl.scan_csv(input_file)
        # 1. Ensure columns are numeric (Float64)
        # strict=False converts unparseable strings to null instead of crashing
        .with_columns([
            pl.col(col).cast(pl.Float64, strict=False) 
            for col in log_cols
        ])
        # 2. Handle volume: if null or 0, make it 1
        .with_columns(
            pl.col("volume").fill_null(1.0).replace(0.0, 1.0)
        )
    )

    processed_df = (
        df
        # 3. Log Returns (Safe now that they are Floats and Volume is non-zero)
        .with_columns([
            (pl.col(col) / pl.col(col).shift(1)).log().alias(col)
            for col in log_cols
        ])
        .drop_nulls()
        
        # 4. Linear Normalization
        .with_columns([
            ((pl.col("year") - YEAR_MIN) / (YEAR_MAX - YEAR_MIN)).alias("year"),
            (pl.col("days") / TOTAL_DAYS_LIMIT).alias("days")
        ])
        
        # 5. Cyclical Encoding
        .with_columns([
            (pl.col("month").cast(pl.Float64) * 2 * np.pi / 12).sin().alias("month_sin"),
            (pl.col("month").cast(pl.Float64) * 2 * np.pi / 12).cos().alias("month_cos"),
            
            (pl.col("day").cast(pl.Float64) * 2 * np.pi / 31).sin().alias("day_sin"),
            (pl.col("day").cast(pl.Float64) * 2 * np.pi / 31).cos().alias("day_cos"),
            
            (pl.col("weekday").cast(pl.Float64) * 2 * np.pi / 7).sin().alias("weekday_sin"),
            (pl.col("weekday").cast(pl.Float64) * 2 * np.pi / 7).cos().alias("weekday_cos"),
        ])
        .drop(["month", "day", "weekday"])
    )

    processed_df.collect().write_csv(output_file)

process_stock_data('./v1-data/MSFT-NASDAQ.csv', './v1-data-ready/MSFT-NASDAQ.csv')