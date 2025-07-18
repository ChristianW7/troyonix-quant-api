"""
Main FastAPI app for Troyonix Quant API.
This app exposes quant strategy endpoints (e.g., moving average crossover).
For informational purposes only. Not financial advice.
"""

from fastapi import FastAPI
from quant_api.routes import moving_average, rsi
from fastapi.openapi.docs import get_swagger_ui_html

app = FastAPI(
    title="Troyonix Quant API",
    description="""
Open-source quant analytics for finance.\n
Informational use only. Not financial advice.
""",
    version="0.1.0"
)

app.include_router(moving_average.router, prefix="/quant")
app.include_router(rsi.router, prefix="/quant")

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title="Troyonix Quant API"
    ) 

@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint to verify the API is running.
    """
    return {"status": "ok"}