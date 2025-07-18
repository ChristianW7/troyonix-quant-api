"""
Relative Strength Index (RSI) Strategy
For informational purposes only. Not financial advice.

This module provides a function to compute the RSI indicator on price data.
"""

import pandas as pd

def calculate_rsi(
    df: pd.DataFrame,
    price_col: str = 'close',
    window: int = 14
) -> pd.DataFrame:
    """
    Calculate the Relative Strength Index (RSI) for a given price series.
    Args:
        df (pd.DataFrame): DataFrame with at least the price_col column.
        price_col (str): Name of the price column (default 'close').
        window (int): Lookback window for RSI calculation (default 14).
    Returns:
        pd.DataFrame: Original DataFrame with an added 'rsi' column.
    """
    # Step 1: Validate input
    if price_col not in df.columns:
        raise ValueError(f"Input DataFrame must contain column: {price_col}")
    if len(df) < window:
        raise ValueError(f"Not enough data: need at least {window} rows, got {len(df)}")

    # Step 2: Make a copy to avoid modifying the original DataFrame
    df = df.copy()

    # Step 3: Calculate price changes (delta)
    df['delta'] = df[price_col].diff()

    # Step 4: Separate gains and losses
    df['gain'] = df['delta'].clip(lower=0)
    df['loss'] = -df['delta'].clip(upper=0)

    # Step 5: Calculate average gain and loss using exponential moving average
    df['avg_gain'] = df['gain'].ewm(alpha=1/window, min_periods=window, adjust=False).mean()
    df['avg_loss'] = df['loss'].ewm(alpha=1/window, min_periods=window, adjust=False).mean()

    # Step 6: Calculate RS (Relative Strength)
    df['rs'] = df['avg_gain'] / df['avg_loss']

    # Step 7: Calculate RSI
    df['rsi'] = 100 - (100 / (1 + df['rs']))

    # Step 8: Clean up intermediate columns
    df = df.drop(columns=['delta', 'gain', 'loss', 'avg_gain', 'avg_loss', 'rs'])

    return df 