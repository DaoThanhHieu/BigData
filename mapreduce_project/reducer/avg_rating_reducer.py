#!/usr/bin/env python3
import sys

total_rating = 0
count = 0

for line in sys.stdin:
    key, value = line.strip().split('\t')
    total_rating += float(value)
    count += 1

if count > 0:
    print(f"Average Rating: {total_rating / count:.2f}")
else:
    print("No valid ratings")
