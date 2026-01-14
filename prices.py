from datetime import datetime

import yfinance as yf

TICKERS = [
    "AVGO",
    "BOXX",
    "IBIT",
    "META",
    "METU",
    "MSFT",
    "NVDA",
    "ORCL",
    "QQQ",
    "QQQM",
    "RKLB",
    "SMR",
    "SOFI",
    "TQQQ",
    "UNH",
    "UPRO",
    "VOO",
]
filename = "prices.bean"

try:
    prices = {}

    for ticker in TICKERS:
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
        f.write(
            f"; fetched on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        )

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
