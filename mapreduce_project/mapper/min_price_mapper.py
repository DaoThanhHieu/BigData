#!/usr/bin/env python3
import sys
import json

for line in sys.stdin:
    try:
        record = json.loads(line)
        price = float(record.get('price', 0))
        title = record.get('title', '')
        print(f"min_price\t{price}\t{title}")
    except:
        continue
