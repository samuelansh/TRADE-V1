"""Convert saved Kraken OHLC JSON (fetched via page-fetch tool) into CSV.

Usage: python3 src/kraken_fetch.py data/raw/btc_kraken.json data/raw/btc_kraken_daily.csv
The JSON is the raw Kraken /0/public/OHLC response.
"""
import json
import sys

import pandas as pd


def convert(src, dst):
    raw = json.loads(open(src).read())
    key = [k for k in raw["result"] if k != "last"][0]
    rows = raw["result"][key]
    df = pd.DataFrame(rows, columns=["ts", "open", "high", "low", "close",
                                     "vwap", "volume", "count"])
    df["time"] = pd.to_datetime(df["ts"].astype(int), unit="s").dt.date
    for c in ["open", "high", "low", "close", "vwap", "volume"]:
        df[c] = df[c].astype(float)
    df = df[["time", "open", "high", "low", "close", "vwap", "volume", "count"]]
    # Kraken's last row is the still-forming candle -> drop it
    df = df.iloc[:-1]
    df.to_csv(dst, index=False)
    print(f"{dst}: {len(df)} rows {df['time'].iloc[0]}..{df['time'].iloc[-1]}")


if __name__ == "__main__":
    convert(sys.argv[1], sys.argv[2])
