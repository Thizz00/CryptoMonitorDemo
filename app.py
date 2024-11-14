import time
import requests
from prometheus_client import start_http_server, Gauge, CollectorRegistry
import logging
from typing import Optional, Tuple

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

registry = CollectorRegistry()

ETH_PRICE = Gauge(
    "ethereum_price_usd", "Current price of Ethereum in USD", registry=registry
)
XMR_PRICE = Gauge(
    "monero_price_usd", "Current price of Monero in USD", registry=registry
)

BINANCE_API_URL = "https://api.binance.com/api/v3/ticker/price"


def fetch_prices() -> Tuple[Optional[float], Optional[float]]:

    try:
        eth_params = {"symbol": "ETHUSDT"}
        logger.info("Fetching Ethereum price...")
        eth_response = requests.get(BINANCE_API_URL, params=eth_params)
        if eth_response.status_code != 200:
            logger.error(f"Error fetching Ethereum price: {eth_response.status_code}")
            return None, None

        eth_data = eth_response.json()
        eth_price = float(eth_data["price"])

        monero_params = {"symbol": "XMRUSDT"}
        logger.info("Fetching Monero price...")
        xmr_response = requests.get(BINANCE_API_URL, params=monero_params)
        if xmr_response.status_code != 200:
            logger.error(f"Error fetching Monero price: {xmr_response.status_code}")
            return None, None

        xmr_data = xmr_response.json()
        xmr_price = float(xmr_data["price"])

        logger.info(f"Fetched Ethereum price: ${eth_price}, Monero price: ${xmr_price}")
        return eth_price, xmr_price

    except requests.exceptions.RequestException as e:
        logger.error(f"Error during request: {e}")
        return None, None


def collect_metrics() -> None:

    logger.info("Collecting metrics...")
    eth_price, xmr_price = fetch_prices()

    if eth_price is not None and xmr_price is not None:
        ETH_PRICE.set(eth_price)
        XMR_PRICE.set(xmr_price)
        logger.info(f"Updated prices: Ethereum = ${eth_price}, Monero = ${xmr_price}")
    else:
        logger.error("Failed to fetch one or more cryptocurrency prices.")


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
