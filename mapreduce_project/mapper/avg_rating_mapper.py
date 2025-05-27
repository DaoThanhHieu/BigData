#!/usr/bin/env python3
import sys
import json

for line in sys.stdin:
    try:
        record = json.loads(line)
        rating = float(record.get("rating", 0))
        print(f"avg_rating\t{rating}")
    except:
        continue
