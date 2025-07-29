from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
import os

app = FastAPI()

# Optional CORS middleware (only needed if frontend calls this API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI on Render!"}

@app.get("/stock/{symbol}")
def get_stock_data(symbol: str):
    api_key = os.environ.get("FINNHUB_API_KEY")
    url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={api_key}"
    response = requests.get(url)

    if response.status_code != 200:
        return {"error": "Failed to fetch data"}

    data = response.json()
    return {
        "symbol": symbol,
        "price": data.get("c"),
        "high": data.get("h"),
        "low": data.get("l"),
        "open": data.get("o"),
        "prev_close": data.get("pc")
    }
