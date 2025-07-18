"""
Moving Average Crossover Strategy
For informational purposes only. Not financial advice.

This module provides a function to compute moving average crossovers on price data.
"""

import pandas as pd
from typing import List

def moving_average_crossover(
    df: pd.DataFrame,
    short_window: int = 20,
    long_window: int = 50,
    price_col: str = 'close',
    date_col: str = 'date',
    return_events_only: bool = False  # New argument
) -> pd.DataFrame:
    """
    Calculate moving average crossover signals.
    Args:
        df (pd.DataFrame): DataFrame with at least [date_col, price_col] columns.
        short_window (int): Window for short-term moving average.
        long_window (int): Window for long-term moving average.
        price_col (str): Name of the price column.
        date_col (str): Name of the date column.
        return_events_only (bool): If True, return only rows where a crossover event occurs.
    Returns:
        pd.DataFrame: Original DataFrame with added columns:
            - 'ma_short': Short-term moving average
            - 'ma_long': Long-term moving average
            - 'signal': 1 for bullish, -1 for bearish, 0 otherwise
            - 'crossover': 1 for bullish crossover, -1 for bearish crossover, 0 otherwise
    """
    # Validate that equired colums exist 
    required_columns = {date_col, price_col}
    if not required_columns.issubset(df.columns):
        raise ValueError(f"Input DataFrame must contain columns: {required_columns}")
    
    # Validate that there is enough data for moving averages 
    if len(df) < max(short_window, long_window):
        raise ValueError(
            f"Not enough data: need at least {max(short_window, long_window)} rows, got {len(df)}"
        )    

    # Make copy to avoid modifying the original DataFrame
    df = df.copy()
    df = df.sort_values(by=date_col)

    # Calculate moving averages 
    df['ma_short'] = df[price_col].rolling(window=short_window, min_periods=1).mean()
    df['ma_long'] = df[price_col].rolling(window=long_window, min_periods=1).mean()

    # Generate signal: 1 if short MA > long MA, else 0
    df['signal'] = 0
    df.loc[long_window:, 'signal'] = (
        (df['ma_short'][long_window:] > df['ma_long'][long_window:]).astype(int)
    )

    # Find crossovers: 1 for bullish, -1 for bearish, 0 otherwise 
    df['crossover'] = df['signal'].diff().fillna(0)
    df['crossover'] = df['crossover'].apply(lambda x: 1 if x == 1 else (-1 if x == -1 else 0))

    # If requested, return only rows where a crossover event occurred
    if return_events_only:
        return df[df['crossover'] != 0].reset_index(drop=True)
    return df

# Example usage (for testing):
if __name__ == "__main__":
    # Simulate some price data
    data = {
        'date': pd.date_range(start='2023-01-01', periods=100, freq='D'),
        'close': [100 + i*0.5 + (-1)**i * 2 for i in range(100)]
    }
    df = pd.DataFrame(data)

    # Test: get all rows (default)
    print("== All Rows ==")
    result = moving_average_crossover(df)
    print(result[["date", "close", "ma_short", "ma_long", "crossover"]].tail(20))

    # Test: get only crossover events
    print("\n== Only Crossover Events ==")
    results_events = moving_average_crossover(df, return_events_only=True)
    print(results_events[["date", "close", "ma_short", "ma_long", "crossover"]]) 