#!/usr/bin/env python3
import sys

total_price = 0.0
count = 0

for line in sys.stdin:
    try:
        key, price, cnt = line.strip().split('\t')
        price = float(price)
        cnt = int(cnt)
        total_price += price
        count += cnt
    except:
        continue

if count > 0:
    print(f"Average_Price\t{total_price/count:.2f}")
else:
    print("Average_Price\t0")
