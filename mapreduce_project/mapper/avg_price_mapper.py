#!/usr/bin/env python3
import sys
import json

for line in sys.stdin:
    try:
        record = json.loads(line)
        price = float(record.get('price', 0))
        print(f"price\t{price}\t1")
    except:
        continue
