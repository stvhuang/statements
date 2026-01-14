from datetime import datetime
from tqdm.auto import tqdm

import yfinance as yf

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
filename = "prices.bean"

try:
    prices = {}

    for ticker in tqdm(TICKERS):
        hist = yf.Ticker(ticker).history(period="1d")

        if not hist.empty:
            prices[ticker] = {
                "price": hist["Close"].iloc[-1],
                "date": hist.index[-1].strftime("%Y-%m-%d"),
            }

    if not prices:
        print("Error: No data retrieved. You may be rate-limited.")
        print("   Try waiting 15 minutes or changing your IP address.")
        exit(1)

    # Write to beancount file
    with open(filename, "w") as f:
        f.write(f"; fetched on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

        for t, data in prices.items():
            price = data["price"]
            date = data["date"]

            if str(price) == "nan":
                print(f"Skipping {t}: Price is NaN")
                continue

            entry = f"{date} price {t} {price:.2f} USD\n"
            f.write(entry)
            print(f"Wrote: {entry.strip()}")

except Exception as e:
    print(f"An unexpected error occurred: {e}")
