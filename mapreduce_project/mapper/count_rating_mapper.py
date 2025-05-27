#!/usr/bin/env python3
import sys
import json

for line in sys.stdin:
    try:
        book = json.loads(line)
        rating = book.get("rating", None)
        if rating is not None:
            print(f"{rating}\t1")
    except:
        continue
