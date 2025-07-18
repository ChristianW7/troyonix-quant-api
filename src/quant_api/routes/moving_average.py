"""
FastAPI route for Moving Average Crossover quant strategy.
For informational purposes only. Not financial advice.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
import pandas as pd
from typing import List
from quant.moving_average_crossover import moving_average_crossover

# Create a router object for this group of endpoints
router = APIRouter()

# Define the expected input data format using Pydantic
class PriceDataRequest(BaseModel):
    return_events_only: bool = Field(False, description="Return only crossover events if True")
    dates: List[str] = Field(..., description="List of date strings (YYYY-MM-DD)")
    closes: List[float] = Field(..., description="List of closing prices (same length as dates)")
    short_window: int = Field(20, description="Short-term moving average window (default 20)")
    long_window: int = Field(50, description="Long-term moving average window (default 50)")

# Define the API endpoint
@router.post("/moving-average-crossover")
def moving_average_crossover_endpoint(request: PriceDataRequest):
    """
    Calculate moving average crossover signals from price data.
    Returns a list of signals and a disclaimer.
    """
    # 1. Validate input lengths
    if len(request.dates) != len(request.closes):
        raise HTTPException(status_code=400, detail="dates and closes must be the same length")
    # 2. Create a DataFrame from the input
    df = pd.DataFrame({"date": request.dates, "close": request.closes})
    # 3. Call the quant strategy function
    result = moving_average_crossover(
        df, 
        request.short_window, 
        request.long_window,
        return_events_only=request.return_events_only
    )
    # 4. Prepare output: only show relevant columns and last 20 rows for brevity
    if request.return_events_only:
        output = result[["date", "close", "ma_short", "ma_long", "crossover"]].to_dict(orient="records")
    else:
        output = result[["date", "close", "ma_short", "ma_long", "crossover"]].tail(20).to_dict(orient="records")
    return {
        "disclaimer": "For informational purposes only. Not financial advice.",
        "signals": output
    } 