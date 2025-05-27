#!/usr/bin/env python3
import sys

min_price = float('inf')
min_title = ""

for line in sys.stdin:
    try:
        key, price, title = line.strip().split('\t', 2)
        price = float(price)
        if price < min_price:
            min_price = price
            min_title = title
    except:
        continue

print(f"Min_Price\t{min_price}\t{min_title}")
