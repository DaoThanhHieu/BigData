#!/usr/bin/env python3
import sys

current_rating = None
count = 0

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    rating, value = line.split("\t")
    try:
        value = int(value)
        if rating == current_rating:
            count += value
        else:
            if current_rating is not None:
                print(f"{current_rating}\t{count}")
            current_rating = rating
            count = value
    except:
        continue

# In dòng cuối cùng
if current_rating is not None:
    print(f"{current_rating}\t{count}")
