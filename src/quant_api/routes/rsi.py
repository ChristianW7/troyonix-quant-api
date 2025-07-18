"""
FastAPI route for Relative Strength Index (RSI) quant strategy.
For informational purposes only. Not financial advice.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
import pandas as pd
from typing import List
from quant.rsi import calculate_rsi

router = APIRouter()

class PriceDataRequest(BaseModel):
    dates: List[str] = Field(..., description="List of date strings (YYYY-MM-DD)")
    closes: List[float] = Field(..., description="List of closing prices (same length as dates)")
    window: int = Field(14, description="RSI window (default 14)")

@router.post("/rsi")
def rsi_endpoint(request: PriceDataRequest):
    """
    Calculate RSI values from price data.
    Returns a list of RSI values and a disclaimer.
    """
    if len(request.dates) != len(request.closes):
        raise HTTPException(status_code=400, detail="dates and closes must be the same length")
    df = pd.DataFrame({"date": request.dates, "close": request.closes})
    try:
        result = calculate_rsi(df, price_col="close", window=request.window)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    output = result[["date", "close", "rsi"]].to_dict(orient="records")
    return {
        "disclaimer": "For informational purposes only. Not financial advice.",
        "rsi": output
    } 