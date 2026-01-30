import yfinance as yf

def fetch_stock(symbol, start="2020-01-01", end="2025-01-01"):
    stock = yf.download(symbol, start=start, end=end)
    stock.to_csv(f"data/{symbol}.csv")
    return stock

if __name__ == "__main__":
    sym = input("Enter stock symbol: ")
    fetch_stock(sym)
