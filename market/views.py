import ccxt
from django.shortcuts import render
from datetime import datetime

# Inicializar Binance
exchange = ccxt.binance()

def btc_chart(request):
    """Gráfico detallado de BTC/USDT con últimas 50 velas"""
    ohlcv = exchange.fetch_ohlcv("BTC/USDT", timeframe="1h", limit=50)

    fechas = [exchange.iso8601(candle[0]) for candle in ohlcv]
    precios = [candle[4] for candle in ohlcv]  # precio de cierre

    return render(request, "market/chart.html", {
        "labels": fechas,
        "values": precios,
    })


def format_time(iso_date: str) -> str:
    """Convierte fecha ISO en formato Año-Mes-Día (ej: 2025-09-19)."""
    dt = datetime.fromisoformat(iso_date.replace("Z", "+00:00"))
    return dt.strftime("%Y-%m-%d")


def dashboard(request):
    """Dashboard ejecutivo con precios reales y velas"""
    # Precio actual de BTC y ETH
    btc_ticker = exchange.fetch_ticker("BTC/USDT")
    eth_ticker = exchange.fetch_ticker("ETH/USDT")

    btc_price = round(btc_ticker["last"], 2)
    eth_price = round(eth_ticker["last"], 2)

    # Velas BTC
    btc_ohlcv = exchange.fetch_ohlcv("BTC/USDT", timeframe="1h", limit=50)
    btc_labels = [format_time(exchange.iso8601(c[0])) for c in btc_ohlcv]
    btc_values = [c[4] for c in btc_ohlcv]

    # Velas ETH
    eth_ohlcv = exchange.fetch_ohlcv("ETH/USDT", timeframe="1h", limit=50)
    eth_labels = [format_time(exchange.iso8601(c[0])) for c in eth_ohlcv]
    eth_values = [c[4] for c in eth_ohlcv]

    # Noticias dummy
    news = [
        {"title": "Bitcoin sube tras decisión de la Fed", "url": "#", "source": "Bloomberg"},
        {"title": "Ethereum con fuerte entrada institucional", "url": "#", "source": "CoinDesk"},
    ]

    context = {
        "btc_price": btc_price,
        "eth_price": eth_price,
        "btc_labels": btc_labels,
        "btc_values": btc_values,
        "eth_labels": eth_labels,
        "eth_values": eth_values,
        "news": news,
        "bot_status": "Activo"
    }
    return render(request, "dashboard.html", context)
