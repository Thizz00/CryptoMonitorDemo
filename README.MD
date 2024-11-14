<img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54"/> <img src="https://img.shields.io/badge/Prometheus-E6522C?style=for-the-badge&logo=Prometheus&logoColor=white"/> <img src="https://img.shields.io/badge/grafana-%23F46800.svg?style=for-the-badge&logo=grafana&logoColor=white"/>

## Brief

An example of an application that allows you to download data for **Ethereum** and **Monero** cryptocurrencies from the Binance API. Metrics are collected by **Prometheus** and then presented on the dashboard in **Graphana** in real time.
The data is downloaded with a delay of several minutes.

![App Screenshot](/docs/dashboard.png)

## Installing

Clone the project:

```bash
  git clone https://github.com/Thizz00/CryptoMonitorDemo.git
```

Deploy with docker compose:

``` bash
docker-compose up --build       
```
