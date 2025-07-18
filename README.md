# Troyonix Quant API

Open-source quantitative finance API for analytics, research, and prototyping.  
**For informational purposes only. Not financial advice.**

## What is this?

The Troyonix Quant API provides easy, programmatic access to classic quantitative trading strategies via a modern REST API.  
It is designed for wealth managers, financial analysts, researchers, and developers who want to analyze price data and generate trading signals—without reinventing the wheel.

## Features

- Moving Average Crossover endpoint
- RSI (Relative Strength Index) endpoint
- FastAPI-powered, interactive docs at `/docs`
- Health check endpoint at `/health`
- Open source, extensible, and ready for production use

## Quickstart

```bash
# Install dependencies
pip install -r requirements.txt

# Run the API (from project root)
uvicorn src.quant_api.main:app --reload
```

Visit [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for interactive API documentation.

## 📈 API Endpoints

### Health Check

`GET /health`  
Returns `{ "status": "ok" }` if the API is running.

### Moving Average Crossover

`POST /quant/moving-average-crossover`

**Request Example:**
```json
{
  "dates": ["2023-01-01", "2023-01-02", "2023-01-03"],
  "closes": [100, 101, 102],
  "short_window": 2,
  "long_window": 3,
  "return_events_only": false
}
```

### RSI

`POST /quant/rsi`

**Request Example:**
```json
{
  "dates": ["2023-01-01", "2023-01-02", "2023-01-03"],
  "closes": [100, 101, 102],
  "window": 14
}
```

## Disclaimer

For informational purposes only. Not financial advice.  
Use at your own risk.

## 📄 License

MIT

## 🤝 Contributing

Pull requests and issues are welcome!
See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines (optional).

---

**Troyonix — Building open, transparent tools for the future of finance.**
