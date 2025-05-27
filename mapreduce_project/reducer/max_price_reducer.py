#!/usr/bin/env python3
import sys

max_price = -1
max_title = ""

for line in sys.stdin:
    try:
        key, price, title = line.strip().split('\t', 2)
        price = float(price)
        if price > max_price:
            max_price = price
            max_title = title
    except:
        continue

print(f"Max_Price\t{max_price}\t{max_title}")

