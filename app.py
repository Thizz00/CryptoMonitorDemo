import time
import requests
from prometheus_client import start_http_server, Gauge, CollectorRegistry
import logging
from typing import Optional, List

BINANCE_API_URL = "https://api.binance.com/api/v3/ticker/price"

CRYPTO_LIST = [
    "ETHUSDT",
    "XMRUSDT",
    "BTCUSDT",
    "DOGEUSDT",
    "PEPEUSDT",
    "SOLUSDT",
    "TRUMPUSDT",
    "XRPUSDT",
    "LTCUSDT",
]

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

registry = CollectorRegistry()

crypto_gauges = {
    symbol: Gauge(
        f"{symbol.lower()}_price_usd",
        f"Current price of {symbol} in USD",
        registry=registry,
    )
    for symbol in CRYPTO_LIST
}


def get_price(symbol: str) -> Optional[float]:
    try:
        response = requests.get(BINANCE_API_URL, params={"symbol": symbol})
        response.raise_for_status()
        data = response.json()
        return float(data["price"])
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching price for {symbol}: {e}")
        return None


def fetch_prices() -> dict:
    prices = {}
    for symbol in CRYPTO_LIST:
        price = get_price(symbol)
        if price is not None:
            prices[symbol] = price
    return prices


def collect_metrics() -> None:
    logger.info("Collecting metrics...")
    prices = fetch_prices()

    if prices:
        for symbol, price in prices.items():
            crypto_gauges[symbol].set(price)
        logger.info(
            "Updated prices: "
            + ", ".join([f"{symbol}=${price}" for symbol, price in prices.items()])
        )
    else:
        logger.error("Failed to fetch cryptocurrency prices.")


def run_metrics_server() -> None:
    logger.info("Starting Prometheus metrics server on port 8000...")
    start_http_server(8000, registry=registry)
    logger.info("Prometheus metrics server started on port 8000")

    while True:
        collect_metrics()
        logger.info("Sleeping for 120 seconds before fetching prices again...")
        time.sleep(120)


if __name__ == "__main__":
    run_metrics_server()
