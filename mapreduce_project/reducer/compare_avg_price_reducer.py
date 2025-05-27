#!/usr/bin/env python3
import sys

sum_books = 0.0
count_books = 0
sum_tiki = 0.0
count_tiki = 0

for line in sys.stdin:
    try:
        tag, price, cnt = line.strip().split('\t')
        price = float(price)
        cnt = int(cnt)
        if tag == 'books':
            sum_books += price
            count_books += cnt
        elif tag == 'tiki':
            sum_tiki += price
            count_tiki += cnt
    except:
        continue

avg_books = sum_books / count_books if count_books > 0 else 0
avg_tiki = sum_tiki / count_tiki if count_tiki > 0 else 0

print(f"Books_Avg_Price\t{avg_books:.2f}")
print(f"Tiki_Avg_Price\t{avg_tiki:.2f}")

