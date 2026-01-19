from datetime import datetime

import yfinance as yf
from tqdm.auto import tqdm

TICKERS = [
    "AAPL",
    "AMZN",
    "AVGO",
    "BOXX",
    "GLD",
    "GOOG",
    "GOOGL",
    "IBIT",
    "META",
    "METU",
    "MSFT",
    "NFLX",
    "NVDA",
    "ORCL",
    "QQQ",
    "QQQM",
    "RKLB",
    "SMR",
    "SOFI",
    "TQQQ",
    "TSLA",
    "TSM",
    "UNH",
    "UPRO",
    "VOO",
]
CURRENCIES = [
    "CNY",
    "IDR",
    "INR",
    "NZD",
    "SGD",
    "TWD",
]
FILENAME = "prices.bean"

try:
    prices = {}

    for ticker in tqdm(TICKERS):
        hist = yf.Ticker(ticker).history(period="1d")

        if not hist.empty:
            prices[ticker] = {
                "price": hist["Close"].iloc[-1],
                "date": hist.index[-1].strftime("%Y-%m-%d"),
            }

    currency_prices_usd = {}

    for currency in tqdm(CURRENCIES):
        symbol = f"{currency}USD=X"
        hist = yf.Ticker(symbol).history(period="1d")

        if not hist.empty:
            currency_prices_usd[currency] = {
                "price": hist["Close"].iloc[-1],
                "date": hist.index[-1].strftime("%Y-%m-%d"),
            }

    currency_prices_twd = {}
    currencies_vs_twd = [c for c in CURRENCIES if c != "TWD"] + ["USD"]

    for currency in tqdm(currencies_vs_twd):
        symbol = f"{currency}TWD=X"
        hist = yf.Ticker(symbol).history(period="1d")

        if not hist.empty:
            currency_prices_twd[currency] = {
                "price": hist["Close"].iloc[-1],
                "date": hist.index[-1].strftime("%Y-%m-%d"),
            }

    if not prices and not currency_prices_usd and not currency_prices_twd:
        print("Error: No data retrieved. You may be rate-limited.")
        print("   Try waiting 15 minutes or changing your IP address.")
        exit(1)

    # Write to beancount file
    with open(FILENAME, "w") as f:
        f.write(f"; {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

        for t, data in prices.items():
            price = data["price"]
            date = data["date"]

            if str(price) == "nan":
                print(f"Skipping {t}: Price is NaN")
                continue

            entry = f"{date} price {t} {price:.2f} USD\n"
            f.write(entry)
            print(f"Wrote: {entry.strip()}")

        for currency, data in currency_prices_usd.items():
            price = data["price"]
            date = data["date"]

            if str(price) == "nan":
                print(f"Skipping {currency}: Price is NaN")
                continue

            entry = f"{date} price {currency} {price:.6f} USD\n"
            f.write(entry)
            print(f"Wrote: {entry.strip()}")

        for currency, data in currency_prices_twd.items():
            price = data["price"]
            date = data["date"]

            if str(price) == "nan":
                print(f"Skipping {currency}: Price is NaN")
                continue

            entry = f"{date} price {currency} {price:.4f} TWD\n"
            f.write(entry)
            print(f"Wrote: {entry.strip()}")

except Exception as e:
    print(f"An unexpected error occurred: {e}")
